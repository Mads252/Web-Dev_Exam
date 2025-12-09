from datetime import datetime

from flask import session
from db import db
from services.user_service import get_user_by_username
from debug import ic


def toggle_follow_by_username(username: str):
    """
    Toggles follow/unfollow for a given target username.

    Rules:
    - User must be logged in.
    - Target user must exist and not be deleted.
    - A user cannot follow themselves.
    - If a follow row already exists → unfollow (delete row).
      Otherwise → follow (insert row with timestamp).
    """
    ic("toggle_follow_by_username", username)

    current_user_id = session.get("user_id")
    if not current_user_id:
        return {
            "ok": False,
            "error": "You must be logged in to follow users.",
        }

    # Load the target user by username
    target_user = get_user_by_username(username)
    ic("target_user", target_user)

    if not target_user or target_user["is_deleted"]:
        return {
            "ok": False,
            "error": "User not found.",
        }

    target_user_id = target_user["user_id"]

    # Prevent following your own account
    if target_user_id == current_user_id:
        return {
            "ok": False,
            "error": "You cannot follow yourself.",
        }

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        # Check if a follow relationship already exists
        cursor.execute(
            """
            SELECT follower_user_id_fk, followee_user_id_fk
            FROM follows
            WHERE follower_user_id_fk = %s AND followee_user_id_fk = %s
            """,
            (current_user_id, target_user_id),
        )

        existing = cursor.fetchone()

        if existing:
            # Unfollow: remove the row
            ic(current_user_id, "stopped following", target_user_id)
            cursor.execute(
                """
                DELETE FROM follows
                WHERE follower_user_id_fk = %s AND followee_user_id_fk = %s
                """,
                (current_user_id, target_user_id),
            )
        else:
            # Follow: insert a new relationship with timestamp
            now = datetime.utcnow()
            epoch_now = now.timestamp()

            ic("Following", current_user_id, "->", target_user_id)
            cursor.execute(
                """
                INSERT INTO follows ( follower_user_id_fk, followee_user_id_fk, created_at )
                VALUES (%s,%s,%s)
                """,
                (current_user_id, target_user_id, epoch_now),
            )

        connection.commit()
        return {
            "ok": True,
            "followee_user_id": target_user_id,
        }

    except Exception as ex:
        ic("TOGGLE FOLLOW EXCEPTION", ex)
        if connection:
            connection.rollback()
        return {
            "ok": False,
            "error": "Unexpected error while toggling follow.",
        }

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass
