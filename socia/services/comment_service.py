import uuid
from datetime import datetime

from flask import request, session
from db import db
from validators import validate_comment_content, ValidationError
from services.post_service import get_post_by_id
from debug import ic


def create_comment(post_id: str):
    """
    Creates a new comment on a post.
    - Requires a logged-in user.
    - Validates that the post exists and is not deleted/blocked.
    - Validates comment content using shared validators.
    """
    ic("create_comment triggered", post_id)

    user_id = session.get("user_id")
    if not user_id:
        return {
            "ok": False,
            "error": "You must be logged in to comment.",
        }

    # Ensure the post exists and is visible
    post = get_post_by_id(post_id)
    if not post or post["is_deleted"] or post["is_blocked"]:
        return {
            "ok": False,
            "error": "Post not found.",
        }

    content = request.form.get("content")
    ic("comment content", content)

    # Validate comment text (length, empty, etc.)
    try:
        content = validate_comment_content(content)
    except ValidationError as ve:
        ic("Comment validation error", ve)
        return {
            "ok": False,
            "error": str(ve),
        }

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        comment_id = uuid.uuid4().hex
        now = datetime.utcnow()
        epoch_now = now.timestamp()

        ic("Inserting new comment", comment_id)
        cursor.execute(
            """
            INSERT INTO comments ( comment_id, post_id_fk, user_id_fk, content, is_deleted, created_at )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (comment_id, post_id, user_id, content, 0, epoch_now),
        )

        connection.commit()
        ic("Comment committed OK")

        return {"ok": True, "comment_id": comment_id}

    except Exception as ex:
        ic("CREATE COMMENT EXCEPTION", ex)
        if connection:
            connection.rollback()
        return {
            "ok": False,
            "error": "Unexpected error while creating comment.",
        }

    finally:
        # Always close DB resources
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def delete_comment(comment_id: str):
    """
    Soft-deletes a comment.
    - Only the comment owner or an admin can delete.
    - Marks the comment as deleted instead of removing the row.
    """
    ic("delete_comment triggered", comment_id)

    user_id = session.get("user_id")
    is_admin = bool(session.get("is_admin"))

    if not user_id:
        return {
            "ok": False,
            "error": "You must be logged in to delete a comment.",
        }

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT comment_id, user_id_fk, is_deleted
            FROM comments
            WHERE comment_id = %s
            LIMIT 1
            """,
            (comment_id,),
        )

        comment = cursor.fetchone()
        ic("Loaded comment", comment)

        if not comment or comment["is_deleted"]:
            return {
                "ok": False,
                "error": "Comment not found.",
            }

        # Only author or admin may delete this comment
        if comment["user_id_fk"] != user_id and not is_admin:
            return {
                "ok": False,
                "error": "You are not allowed to delete this comment.",
            }

        ic("Soft deleting comment", comment_id)

        cursor.execute(
            """
            UPDATE comments
            SET is_deleted = 1
            WHERE comment_id = %s
            """,
            (comment_id,),
        )

        connection.commit()
        ic("Comment soft-deleted OK")

        return {"ok": True}

    except Exception as ex:
        ic("DELETE COMMENT EXCEPTION", ex)
        if connection:
            connection.rollback()
        return {
            "ok": False,
            "error": "Unexpected error while deleting comment.",
        }

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


from db import db  # kept for clarity, although already imported above
from debug import ic  # same here, used throughout this module


def get_comments_for_post(post_id: str):
    """
    Loads all non-deleted comments for a given post, together with user info.
    Returns a list of objects in the shape:
      {
        "comment": {...},
        "user": {...}
      }
    which is convenient for the Jinja partial template.
    """
    ic("get_comments_for_post", post_id)

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT c.comment_id, c.post_id_fk, c.user_id_fk, c.content, c.created_at, u.username, u.display_name, u.avatar_filename
            FROM comments c
            JOIN users u ON u.user_id = c.user_id_fk
            WHERE c.post_id_fk = %s AND c.is_deleted = 0 AND u.is_deleted = 0
            ORDER BY c.created_at ASC
            """,
            (post_id,),
        )
        rows = cursor.fetchall() or []

        comments = []
        for c in rows:
            comments.append(
                {
                    "comment": {
                        "comment_id": c["comment_id"],
                        "content": c["content"],
                        "created_at": c["created_at"],
                        "user_id_fk": c["user_id_fk"],
                    },
                    "user": {
                        "username": c["username"],
                        "display_name": c["display_name"],
                        "avatar_filename": c["avatar_filename"],
                    },
                }
            )

        return comments

    finally:
        # Safe cleanup even if something fails above
        if cursor:
            cursor.close()
        if connection:
            connection.close()
