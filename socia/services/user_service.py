import os
from datetime import datetime

from flask import request, session, current_app
from werkzeug.utils import secure_filename

from db import db
from validators import (
    validate_display_name,
    validate_bio,
    validate_avatar_file,
    ValidationError,
)
from debug import ic


def get_current_user():
    """
    Returns the currently logged-in user object from the database,
    or None if:
    - no user_id is stored in the session, or
    - the user does not exist, or
    - the user is soft-deleted.
    """
    user_id = session.get("user_id")

    if not user_id:
        ic("No user logged in")
        return None

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
              user_id,
              email,
              username,
              display_name,
              bio,
              avatar_filename,
              is_admin,
              is_blocked,
              is_deleted
            FROM users
            WHERE user_id = %s
            """,
            (user_id,),
        )

        user = cursor.fetchone()

        if not user or user["is_deleted"]:
            return None

        return user

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def get_user_by_username(username: str):
    """
    Loads a user record by username.
    Returns None if the user does not exist or is soft-deleted.
    """
    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
              user_id,
              email,
              username,
              display_name,
              bio,
              avatar_filename,
              is_admin,
              is_blocked,
              is_deleted
            FROM users
            WHERE username = %s
            """,
            (username,),
        )

        user = cursor.fetchone()
        ic("get_user_by_username", username, user)

        if not user or user["is_deleted"]:
            return None

        return user

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def update_profile_and_avatar():
    """
    Updates the current user's profile fields (display_name, bio)
    and optionally their avatar image.

    Flow:
    - Load current user from session.
    - Validate display_name and bio.
    - If avatar uploaded, validate and save it to AVATAR_UPLOAD_FOLDER.
      One avatar per user → filename is user_id + extension.
    - Update users table with new profile data (and avatar if provided).
    """
    current_user = get_current_user()
    if not current_user:
        return {
            "ok": False,
            "error": "You must be logged in to update your profile.",
        }

    display_name = request.form.get("display_name")
    bio = request.form.get("bio")
    avatar_file = request.files.get("avatar")

    ic("Profile update payload", display_name, bio, avatar_file)

    # Validate textual fields
    try:
        display_name = validate_display_name(display_name)
        bio = validate_bio(bio)
    except ValidationError as ve:
        ic("Profile text validation error", ve)
        return {
            "ok": False,
            "error": str(ve),
            "form": {
                "display_name": display_name,
                "bio": bio,
            },
        }

    new_avatar_filename = None

    # If user selected a new avatar, validate and save it
    if avatar_file and avatar_file.filename:
        try:
            validate_avatar_file(avatar_file)
        except ValidationError as ve:
            ic("Avatar validation error", ve)
            return {
                "ok": False,
                "error": str(ve),
                "form": {
                    "display_name": display_name,
                    "bio": bio,
                },
            }

        upload_folder = current_app.config.get(
            "AVATAR_UPLOAD_FOLDER",
            "static/uploads/avatars",
        )
        abs_upload_folder = os.path.join(current_app.root_path, upload_folder)
        os.makedirs(abs_upload_folder, exist_ok=True)

        # One avatar per user: user_id + extension
        _, ext = os.path.splitext(avatar_file.filename.lower())
        new_avatar_filename = f"{current_user['user_id']}{ext}"
        safe_filename = secure_filename(new_avatar_filename)
        save_path = os.path.join(abs_upload_folder, safe_filename)

        ic("Saving avatar to", save_path)
        avatar_file.save(save_path)

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        now = datetime.utcnow()
        epoch_now = now.timestamp()

        if new_avatar_filename is not None:
            # Update profile including new avatar
            cursor.execute(
                """
                UPDATE users
                SET display_name = %s, bio = %s, avatar_filename = %s, updated_at = %s
                WHERE user_id = %s
                """,
                (
                    display_name,
                    bio,
                    new_avatar_filename,
                    epoch_now,
                    current_user["user_id"],
                ),
            )
        else:
            # Update only text profile fields
            ic("Updating profile without avatar change")
            cursor.execute(
                """
                UPDATE users
                SET display_name = %s, bio = %s, updated_at = %s
                WHERE user_id = %s
                """,
                (
                    display_name,
                    bio,
                    epoch_now,
                    current_user["user_id"],
                ),
            )

        connection.commit()
        ic("Profile updates committed")

        return {"ok": True}

    except Exception as ex:
        ic("UPDATE PROFILE EXCEPTION", ex)
        if connection:
            connection.rollback()
        return {
            "ok": False,
            "error": "An unexpected error occurred while updating your profile.",
        }

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def get_follow_stats(user_id: str) -> dict:
    """
    Returns follower/following counts for a given user_id.

    Shape:
      {
        "followers_count": int,
        "following_count": int
      }
    """
    ic("get_follow_stats activated", user_id)

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        # How many users follow this user?
        cursor.execute(
            """
            SELECT COUNT(*) AS c
            FROM follows
            WHERE followee_user_id_fk = %s
            """,
            (user_id,),
        )
        followers_row = cursor.fetchone() or {"c": 0}

        # How many users does this user follow?
        cursor.execute(
            """
            SELECT COUNT(*) AS c
            FROM follows
            WHERE follower_user_id_fk = %s
            """,
            (user_id,),
        )
        following_row = cursor.fetchone() or {"c": 0}

        stats = {
            "followers_count": int(followers_row["c"]),
            "following_count": int(following_row["c"]),
        }
        ic("get_follow_stats result", stats)
        return stats

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def is_following(follower_user_id: str, followee_user_id: str) -> bool:
    """
    Returns True if follower_user_id is following followee_user_id.
    Used to render the correct follow/unfollow button state.
    """
    ic("is_following", follower_user_id, followee_user_id)

    if not follower_user_id or not followee_user_id:
        return False

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT 1
            FROM follows
            WHERE follower_user_id_fk = %s
              AND followee_user_id_fk = %s
            LIMIT 1
            """,
            (follower_user_id, followee_user_id),
        )

        row = cursor.fetchone()
        ic("is_following row", row)

        return row is not None

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def delete_current_user():
    """
    Soft-deletes the currently logged-in user and cleans up related data.

    Steps:
    - Mark user as deleted (users.is_deleted = 1).
    - Soft-delete user's posts (posts.is_deleted = 1).
    - Soft-delete user's comments (comments.is_deleted = 1).
    - Delete likes made by the user.
    - Delete follow relationships where the user is follower or followee.
    """
    ic("delete_current_user triggered")

    user_id = session.get("user_id")
    if not user_id:
        return {
            "ok": False,
            "error": "You must be logged in to delete your account.",
        }

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        # Ensure user exists and is not already deleted
        cursor.execute(
            """
            SELECT user_id, is_deleted
            FROM users
            WHERE user_id = %s
            LIMIT 1
            """,
            (user_id,),
        )
        user = cursor.fetchone()
        ic("User to delete", user)

        if not user or user["is_deleted"]:
            return {
                "ok": False,
                "error": "Account not found.",
            }

        now = datetime.utcnow()
        epoch_now = now.timestamp()

        ic("Soft deleting user and related data", user_id)

        # 1) Soft-delete user
        cursor.execute(
            """
            UPDATE users
            SET is_deleted = 1, updated_at = %s
            WHERE user_id = %s
            """,
            (epoch_now, user_id),
        )

        # 2) Soft-delete user's posts
        cursor.execute(
            """
            UPDATE posts
            SET is_deleted = 1, updated_at = %s
            WHERE user_id_fk = %s
            """,
            (epoch_now, user_id),
        )

        # 3) Soft-delete user's comments
        cursor.execute(
            """
            UPDATE comments
            SET is_deleted = 1
            WHERE user_id_fk = %s
            """,
            (user_id,),
        )

        # 4) Delete likes created by the user
        cursor.execute(
            """
            DELETE FROM likes
            WHERE user_id_fk = %s
            """,
            (user_id,),
        )

        # 5) Delete follows where user is follower or followee
        cursor.execute(
            """
            DELETE FROM follows
            WHERE follower_user_id_fk = %s OR followee_user_id_fk = %s
            """,
            (user_id, user_id),
        )

        connection.commit()
        ic("User and related data soft-deleted OK")

        return {"ok": True}

    except Exception as ex:
        ic("DELETE CURRENT USER EXCEPTION", ex)
        if connection:
            connection.rollback()
        return {
            "ok": False,
            "error": "Unexpected error while deleting your account.",
        }

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass
