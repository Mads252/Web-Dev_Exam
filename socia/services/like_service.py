from datetime import datetime
from flask import session
from db import db
from debug import ic
from services.post_service import get_post_by_id


def toggle_like(post_id: str):
    """
    Toggle a like for a specific post.
    
    Rules:
    - User must be logged in.
    - Post must exist and not be deleted or blocked.
    - If the user already liked the post → unlike (delete row).
      Otherwise → like (insert row timestamped).
    """
    ic("toggle_like triggered", post_id)

    user_id = session.get("user_id")
    if not user_id:
        return {
            "ok": False,
            "error": "You must be logged in to like a post."
        }

    # Validate that the post exists and is visible
    post = get_post_by_id(post_id)
    if not post or post["is_deleted"] or post["is_blocked"]:
        return {
            "ok": False,
            "error": "Post not found."
        }

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        # Check whether the user already liked this post
        cursor.execute(
            """
            SELECT user_id_fk, post_id_fk
            FROM likes
            WHERE user_id_fk = %s AND post_id_fk = %s
            """,
            (user_id, post_id),
        )
        existing = cursor.fetchone()

        if existing:
            # Already liked → unlike
            ic("Unliking post", post_id)
            cursor.execute(
                """
                DELETE FROM likes
                WHERE user_id_fk = %s AND post_id_fk = %s
                """,
                (user_id, post_id),
            )
        else:
            # Not yet liked → insert like
            now = datetime.utcnow()
            epoch_now = now.timestamp()

            ic("Liking post", post_id)
            cursor.execute(
                """
                INSERT INTO likes (user_id_fk, post_id_fk, created_at)
                VALUES (%s, %s, %s)
                """,
                (user_id, post_id, epoch_now),
            )

        connection.commit()
        ic("Like toggled OK")
        return {"ok": True}

    except Exception as ex:
        ic("TOGGLE LIKE EXCEPTION", ex)
        if connection:
            connection.rollback()
        return {
            "ok": False,
            "error": "Unexpected error while toggling like."
        }

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass
