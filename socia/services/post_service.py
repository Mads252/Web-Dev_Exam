import os
import uuid
from datetime import datetime

from flask import request, session, current_app
from werkzeug.utils import secure_filename

from db import db
from validators import (
    validate_post_content,
    validate_post_media_file,
    ValidationError,
)
from debug import ic
#TODO: make sure det user has logged in 
#TODO: valider det postet contet 
#TODO: gem det postet content 
#TODO: indset i databasen

def create_post():
    """
    Creates a new post for the currently logged-in user.

    Rules:
    - User must be logged in.
    - Content is validated (length / allowed chars).
    - At least one of: text content OR one or more media files.
    - Media files are validated and saved to POST_UPLOAD_FOLDER.
    - Post + media are inserted in a single transaction.
    """
    ic("create_post triggered")

    user_id = session.get("user_id")

    # This should normally be caught by the route, but we keep the guard
    if not user_id:
        ic("User not logged in - cannot create post")
        return {
            "ok": False,
            "error": "You must be logged in to create a post.",
        }

    content = request.form.get("content")
    ic("post content", content)

    # Validate post text content
    try:
        content = validate_post_content(content)
    except ValidationError as ve:
        ic("Content validation error", ve)
        return {
            "ok": False,
            "error": str(ve),
            "form": {
                "content": content,
            },
        }

    # Collect uploaded media files (if any)
    media_files = request.files.getlist("media") or []

    # Filter out empty / no-filename entries
    media_files = [f for f in media_files if f and getattr(f, "filename", "")]

    # Require at least text or one image
    if not content and not media_files:
        return {
            "ok": False,
            "error": "Post must contain text or at least one image.",
            "form": {
                "content": content,
            },
        }

    # Validate all selected media files (size, type, etc.)
    try:
        for f in media_files:
            validate_post_media_file(f)
    except ValidationError as ve:
        ic("Media validation error", ve)
        return {
            "ok": False,
            "error": str(ve),
            "form": {
                "content": content,
            },
        }

    connection = None
    cursor = None

    # Insert post and media in one transaction
    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        post_id = uuid.uuid4().hex
        now = datetime.utcnow()
        epoch_now = now.timestamp()

        ic("Inserting post into DB", post_id)

        cursor.execute(
            """
            INSERT INTO posts ( post_id, user_id_fk, content, is_blocked, is_deleted, created_at, updated_at )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                post_id,
                user_id,
                content,
                0,
                0,
                epoch_now,
                epoch_now,
            ),
        )

        # Build absolute path for media upload folder
        upload_folder = current_app.config.get(
            "POST_UPLOAD_FOLDER",
            "static/uploads/posts",
        )
        abs_upload_folder = os.path.join(current_app.root_path, upload_folder)
        os.makedirs(abs_upload_folder, exist_ok=True)

        # Save each media file and insert a post_media row
        for f in media_files:
            original_filename = f.filename
            _, ext = os.path.splitext(original_filename.lower())
            media_id = uuid.uuid4().hex
            new_filename = f"{media_id}{ext}"
            safe_filename = secure_filename(new_filename)
            save_path = os.path.join(abs_upload_folder, safe_filename)

            ic("Saving media file", save_path)
            f.save(save_path)

            # Path stored in DB (relative to app root/static)
            file_path_db = f"{upload_folder}/{safe_filename}"

            cursor.execute(
                """
                INSERT INTO post_media ( media_id, post_id_fk, file_path, media_type, created_at)
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    media_id,
                    post_id,
                    file_path_db,
                    "image",  # currently only images are supported
                    epoch_now,
                ),
            )

        connection.commit()
        ic("Post + media committed")

        return {
            "ok": True,
            "message": "Post created successfully.",
            "post_id": post_id,
        }

    except Exception as ex:
        ic("CREATE POST EXCEPTION", ex)
        if connection:
            connection.rollback()
        return {
            "ok": False,
            "error": "An unexpected error occurred while creating the post.",
            "form": {
                "content": content,
            },
        }

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def get_latest_posts(limit: int = 20, current_user_id: str | None = None):
    """
    Fetches the latest posts for the global feed.

    Behavior:
    - Only non-deleted and non-blocked posts from non-deleted users.
    - Joins user data (username, display_name, avatar).
    - Loads media, likes, and comments in separate queries and groups
      them by post_id.
    - Returns a list of dicts with this structure:
      {
        "post": {...},
        "user": {...},
        "media": [...],
        "like_count": int,
        "liked_by_current_user": bool,
        "comments": [...]
      }
    """
    ic("get_latest_posts triggered", limit)

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        # Base posts + author info
        cursor.execute(
            """
            SELECT p.post_id, p.user_id_fk, p.content, p.created_at, u.username, u.display_name, u.avatar_filename
            FROM posts p
            JOIN users u ON u.user_id = p.user_id_fk
            WHERE p.is_deleted = 0 AND p.is_blocked = 0 AND u.is_deleted = 0
            ORDER BY p.created_at DESC
            LIMIT %s
            """,
            (limit,),
        )

        posts = cursor.fetchall()
        ic("Posts count", len(posts))

        if not posts:
            return []

        post_ids = [row["post_id"] for row in posts]

        # Load media for all posts in one query
        cursor.execute(
            """
            SELECT post_id_fk, file_path, media_type
            FROM post_media
            WHERE post_id_fk IN ({placeholders})
            """.format(placeholders=",".join(["%s"] * len(post_ids))),
            tuple(post_ids),
        )
        media_rows = cursor.fetchall()
        ic("Media rows count", len(media_rows))

        media_by_post = {}
        for m in media_rows:
            media_by_post.setdefault(m["post_id_fk"], []).append(m)

        # Load like counts per post
        cursor.execute(
            """
            SELECT post_id_fk, COUNT(*) AS like_count
            FROM likes
            WHERE post_id_fk IN ({placeholders})
            GROUP BY post_id_fk
            """.format(placeholders=",".join(["%s"] * len(post_ids))),
            tuple(post_ids),
        )
        like_rows = cursor.fetchall()
        ic("Like rows count", len(like_rows))

        like_count_by_post: dict[str, int] = {}
        for row in like_rows:
            like_count_by_post[row["post_id_fk"]] = int(row["like_count"])

        # Which posts are liked by the current user?
        liked_by_current_user_set: set[str] = set()
        if current_user_id:
            cursor.execute(
                """
                SELECT post_id_fk
                FROM likes
                WHERE post_id_fk IN ({placeholders}) AND user_id_fk = %s
                """.format(placeholders=",".join(["%s"] * len(post_ids))),
                tuple(post_ids) + (current_user_id,),
            )
            liked_rows = cursor.fetchall()
            ic("Liked by current user rows", liked_rows)

            liked_by_current_user_set = {row["post_id_fk"] for row in liked_rows}

        # Load comments for all posts
        cursor.execute(
            """
            SELECT c.comment_id, c.post_id_fk, c.user_id_fk, c.content, c.created_at, u.username, u.display_name, u.avatar_filename
            FROM comments c
            JOIN users u ON u.user_id = c.user_id_fk
            WHERE c.post_id_fk IN ({placeholders}) AND c.is_deleted = 0 AND u.is_deleted = 0
            ORDER BY c.created_at ASC
            """.format(placeholders=",".join(["%s"] * len(post_ids))),
            tuple(post_ids),
        )

        comment_rows = cursor.fetchall()
        ic("Comment rows count", len(comment_rows))

        comments_by_post: dict[str, list] = {}
        for c in comment_rows:
            comments_by_post.setdefault(c["post_id_fk"], []).append(
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

        # Build the final feed structure
        result = []
        for p in posts:
            post_id = p["post_id"]
            result.append(
                {
                    "post": p,
                    "user": {
                        "username": p["username"],
                        "display_name": p["display_name"],
                        "avatar_filename": p["avatar_filename"],
                    },
                    "media": media_by_post.get(post_id, []),
                    "like_count": like_count_by_post.get(post_id, 0),
                    "liked_by_current_user": post_id in liked_by_current_user_set,
                    "comments": comments_by_post.get(post_id, []),
                }
            )

        return result

    except Exception as ex:
        ic("GET LATEST POSTS EXCEPTION", ex)
        return []

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def get_latest_posts_from_following(
    follower_user_id: str,
    limit: int = 20,
    offset: int = 0,
):
    """
    Fetches latest posts only from users that `follower_user_id` follows.

    The return structure matches get_latest_posts(), so the same template
    can be reused:
      {
        "post": {...},
        "user": {...},
        "media": [...],
        "like_count": int,
        "liked_by_current_user": bool,
        "comments": [...]
      }
    """
    ic(
        "get_latest_posts_from_following",
        follower_user_id,
        limit,
        offset,
    )

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        # Base posts from followees
        cursor.execute(
            """
            SELECT p.post_id, p.user_id_fk, p.content, p.created_at, p.is_blocked, p.is_deleted
            FROM posts p
            JOIN follows f ON f.followee_user_id_fk = p.user_id_fk
            WHERE f.follower_user_id_fk = %s AND p.is_deleted = 0 AND p.is_blocked = 0
            ORDER BY p.created_at DESC
            LIMIT %s OFFSET %s
            """,
            (follower_user_id, limit, offset),
        )
        post_rows = cursor.fetchall() or []
        ic("following feed - post_rows", len(post_rows))

        if not post_rows:
            return []

        post_ids = [row["post_id"] for row in post_rows]

        # Load user info for all authors in this feed
        cursor.execute(
            """
            SELECT u.user_id, u.username, u.display_name, u.avatar_filename
            FROM users u
            WHERE u.user_id IN (
              SELECT DISTINCT p.user_id_fk
              FROM posts p
              WHERE p.post_id IN ({})
            )
            """.format(",".join(["%s"] * len(post_ids))),
            tuple(post_ids),
        )
        user_rows = cursor.fetchall() or []
        users_by_id = {u["user_id"]: u for u in user_rows}

        # Media for these posts
        cursor.execute(
            """
            SELECT post_id_fk, file_path, media_type
            FROM post_media
            WHERE post_id_fk IN ({})
            """.format(",".join(["%s"] * len(post_ids))),
            tuple(post_ids),
        )
        media_rows = cursor.fetchall() or []
        media_by_post = {}
        for m in media_rows:
            media_by_post.setdefault(m["post_id_fk"], []).append(m)

        # Like counts per post
        cursor.execute(
            """
            SELECT post_id_fk, COUNT(*) AS like_count
            FROM likes
            WHERE post_id_fk IN ({})
            GROUP BY post_id_fk
            """.format(",".join(["%s"] * len(post_ids))),
            tuple(post_ids),
        )
        likes_rows = cursor.fetchall() or []
        likes_by_post = {
            row["post_id_fk"]: int(row["like_count"]) for row in likes_rows
        }

        # Posts liked by the follower user
        cursor.execute(
            """
            SELECT post_id_fk
            FROM likes
            WHERE post_id_fk IN ({})
              AND user_id_fk = %s
            """.format(",".join(["%s"] * len(post_ids))),
            tuple(post_ids) + (follower_user_id,),
        )
        liked_rows = cursor.fetchall() or []
        liked_posts = {row["post_id_fk"] for row in liked_rows}

        # Load comments via dedicated service for consistency
        from services.comment_service import get_comments_for_post

        items = []
        for p in post_rows:
            pid = p["post_id"]
            uid = p["user_id_fk"]
            user = users_by_id.get(uid, {})

            comments = get_comments_for_post(pid)

            items.append(
                {
                    "post": {
                        "post_id": pid,
                        "user_id_fk": uid,
                        "content": p["content"],
                        "created_at": p["created_at"],
                    },
                    "user": {
                        "username": user.get("username"),
                        "display_name": user.get("display_name"),
                        "avatar_filename": user.get("avatar_filename"),
                    },
                    "media": media_by_post.get(pid, []),
                    "like_count": likes_by_post.get(pid, 0),
                    "liked_by_current_user": pid in liked_posts,
                    "comments": comments,
                }
            )

        return items

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_post_by_id(post_id: str):
    """
    Loads a single post row by ID.
    Used for permission checks and edit/delete operations.
    """
    ic("get_post_by_id triggered", post_id)

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT post_id, user_id_fk, content, is_blocked, is_deleted, created_at, updated_at
            FROM posts
            WHERE post_id = %s
            LIMIT 1
            """,
            (post_id,),
        )

        post = cursor.fetchone()
        ic("get_post_by_id result", post)
        return post

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def update_post(post_id: str):
    """
    Updates the content of an existing post.

    Rules:
    - User must be logged in.
    - Only the post owner or an admin may edit.
    - New content is validated and cannot be empty.
    """
    ic("update_post triggered", post_id)

    user_id = session.get("user_id")
    is_admin = bool(session.get("is_admin"))

    if not user_id:
        return {
            "ok": False,
            "error": "You must be logged in to edit a post.",
        }

    post = get_post_by_id(post_id)
    if not post:
        return {
            "ok": False,
            "error": "Post not found.",
        }

    # Permission check: owner or admin only
    if post["user_id_fk"] != user_id and not is_admin:
        return {
            "ok": False,
            "error": "You are not allowed to edit this post.",
        }

    new_content = request.form.get("content")
    ic("New content", new_content)

    try:
        new_content = validate_post_content(new_content)
    except ValidationError as ve:
        ic("Update post validation error", ve)
        return {
            "ok": False,
            "error": str(ve),
            "form": {
                "content": new_content,
            },
        }

    if not new_content:
        return {
            "ok": False,
            "error": "Post content cannot be empty when editing.",
            "form": {
                "content": new_content,
            },
        }

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        now = datetime.utcnow()
        epoch_now = now.timestamp()

        cursor.execute(
            """
            UPDATE posts
            SET content = %s,
                updated_at = %s
            WHERE post_id = %s
            """,
            (new_content, epoch_now, post_id),
        )

        connection.commit()
        ic("Post updated OK")

        return {
            "ok": True,
            "post_id": post_id,
        }

    except Exception as ex:
        ic("UPDATE POST EXCEPTION", ex)
        if connection:
            connection.rollback()
        return {
            "ok": False,
            "error": "An unexpected error occurred while updating the post.",
        }

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def delete_post(post_id: str):
    """
    Soft-deletes a post by setting is_deleted = 1.

    Rules:
    - User must be owner or admin.
    - Post must exist and not already be deleted.
    """
    ic("delete_post triggered", post_id)

    user_id = session.get("user_id")
    is_admin = bool(session.get("is_admin"))

    post = get_post_by_id(post_id)
    if not post or post["is_deleted"]:
        return {
            "ok": False,
            "error": "Post not found.",
        }

    if post["user_id_fk"] != user_id and not is_admin:
        return {
            "ok": False,
            "error": "You are not allowed to delete this post.",
        }

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        now = datetime.utcnow()
        epoch_now = now.timestamp()

        cursor.execute(
            """
            UPDATE posts
            SET is_deleted = 1,
                updated_at = %s
            WHERE post_id = %s
            """,
            (epoch_now, post_id),
        )

        connection.commit()
        ic("Post soft-deleted OK")

        return {"ok": True}

    except Exception as ex:
        ic("DELETE POST EXCEPTION", ex)
        if connection:
            connection.rollback()
        return {
            "ok": False,
            "error": "An unexpected error occurred while deleting the post.",
        }

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def get_like_state_for_post(post_id: str, current_user_id: str | None = None):
    """
    Returns the like state for a single post:
    - like_count: total number of likes
    - liked_by_current_user: whether the given user has liked this post

    This is used by the MixHTML like endpoint to re-render only the like block.
    """
    ic("get_like_state_for_post", post_id, current_user_id)

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        # Total like count
        cursor.execute(
            """
            SELECT COUNT(*) AS like_count
            FROM likes
            WHERE post_id_fk = %s
            """,
            (post_id,),
        )
        row = cursor.fetchone() or {"like_count": 0}
        like_count = int(row["like_count"])

        liked_by_current_user = False
        if current_user_id:
            cursor.execute(
                """
                SELECT 1
                FROM likes
                WHERE post_id_fk = %s
                  AND user_id_fk = %s
                LIMIT 1
                """,
                (post_id, current_user_id),
            )
            liked_row = cursor.fetchone()
            liked_by_current_user = liked_row is not None

        return {
            "like_count": like_count,
            "liked_by_current_user": liked_by_current_user,
        }

    except Exception as ex:
        ic("GET LIKE STATE EXCEPTION", ex)
        # Safe fallback: treat as no likes
        return {
            "like_count": 0,
            "liked_by_current_user": False,
        }

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass
