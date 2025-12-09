from datetime import datetime

from db import db
from debug import ic
from mail_service import send_user_block_email, send_post_block_email


def _require_connection():
    """
    Small helper to open a DB connection with a dictionary cursor.
    Used by all admin service functions to avoid repeating boilerplate.
    """
    connection = db()
    cursor = connection.cursor(dictionary=True)
    return connection, cursor


def get_all_users():
    """
    Returns a list of all users for the admin user table.
    Includes flags for admin, blocked and deleted state.
    """
    connection, cursor = _require_connection()
    try:
        cursor.execute(
            """
            SELECT user_id, email, username, display_name, is_admin, is_blocked, is_deleted, created_at
            FROM users
            ORDER BY created_at DESC
            """
        )

        users = cursor.fetchall()
        ic("get_all_users count", len(users))
        return users

    finally:
        # Always clean up DB resources
        cursor.close()
        connection.close()


def get_recent_posts(limit: int = 50):
    """
    Returns latest posts (with author info) for the admin posts table.
    Limit is used to protect performance in the admin UI.
    """
    connection, cursor = _require_connection()
    try:
        cursor.execute(
            """
            SELECT p.post_id, p.user_id_fk, p.content, p.is_blocked, p.is_deleted, p.created_at, u.username, u.email
            FROM posts p
            JOIN users u ON u.user_id = p.user_id_fk
            ORDER BY p.created_at DESC
            LIMIT %s
            """,
            (limit,),
        )

        posts = cursor.fetchall()
        ic("get_recent_posts count", len(posts))
        return posts

    finally:
        cursor.close()
        connection.close()


def toggle_user_block(user_id: str):
    """
    Toggles a user's blocked state.
    - If the user is blocked after the change, a notification email is sent.
    - Deleted users cannot be blocked/unblocked.
    """
    ic("toggle user block is triggered")

    connection, cursor = _require_connection()
    try:
        cursor.execute(
            """
            SELECT user_id, email, is_blocked, is_deleted
            FROM users
            WHERE user_id = %s
            LIMIT 1
            """,
            (user_id,),
        )

        user = cursor.fetchone()
        ic("User to toggle block", user)

        if not user or user["is_deleted"]:
            return {
                "ok": False,
                "error": "User not found.",
            }

        now = datetime.utcnow()
        epoch_now = now.timestamp()

        # Flip the blocked state: 0 → 1, 1 → 0
        new_block_state = 0 if user["is_blocked"] else 1

        cursor.execute(
            """
            UPDATE users
            SET is_blocked = %s, updated_at = %s
            WHERE user_id = %s
            """,
            (new_block_state, epoch_now, user_id),
        )

        connection.commit()
        ic("User block toggled", new_block_state)

        # Only send email when the user becomes blocked (not when unblocked)
        if new_block_state == 1:
            send_user_block_email(user["email"])

        return {
            "ok": True,
            "is_blocked": bool(new_block_state),
        }

    except Exception as ex:
        ic("TOGGLE_USER_BLOCK EXCEPTION", ex)
        connection.rollback()
        return {
            "ok": False,
            "error": "Unexpected error while updating user block state.",
        }

    finally:
        cursor.close()
        connection.close()


def toggle_post_block(post_id: str):
    """
    Toggles block/unblock on a post.
    - Deleted posts cannot be blocked/unblocked.
    - When a post is blocked, an email is sent to the author with a short preview.
    """
    ic("toggle_post_block triggered", post_id)

    connection, cursor = _require_connection()
    try:
        cursor.execute(
            """
            SELECT p.post_id, p.content, p.is_blocked, p.is_deleted, u.email
            FROM posts p
            JOIN users u ON u.user_id = p.user_id_fk
            WHERE p.post_id = %s
            LIMIT 1
            """,
            (post_id,),
        )
        row = cursor.fetchone()
        ic("Post to toggle block", row)

        if not row or row["is_deleted"]:
            return {
                "ok": False,
                "error": "Post not found.",
            }

        now = datetime.utcnow()
        epoch_now = now.timestamp()

        # Flip the blocked state for the post
        new_block_state = 0 if row["is_blocked"] else 1

        cursor.execute(
            """
            UPDATE posts
            SET is_blocked = %s, updated_at = %s
            WHERE post_id = %s
            """,
            (new_block_state, epoch_now, post_id),
        )

        connection.commit()
        ic("Post block toggled", new_block_state)

        if new_block_state == 1:
            # Build a short preview of the post content for the email
            content = row["content"] or ""
            preview = content[:120] + ("..." if len(content) > 120 else "")
            send_post_block_email(row["email"], preview)

        return {
            "ok": True,
            "is_blocked": bool(new_block_state),
        }

    except Exception as ex:
        ic("TOGGLE_POST_BLOCK EXCEPTION", ex)
        connection.rollback()
        return {
            "ok": False,
            "error": "Unexpected error while updating post block state.",
        }

    finally:
        cursor.close()
        connection.close()
