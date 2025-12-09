# services/auth_service.py
import uuid
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, session
from db import db
from validators import (
    validate_email,
    validate_username,
    validate_password,
    ValidationError,
)
from mail_service import send_verification_email, send_password_reset_email
from debug import ic

# Lifetime of email verification links (in seconds)
VERIFICATION_TIME = 86400  # 24 hours
# Lifetime of password reset links (in seconds)
RESET_PASSWORD_TIME = 7200  # 2 hours


def signup():
    """
    Handles sign-up logic:
    - Validates email/username/password.
    - Ensures email and username are unique.
    - Inserts user and email_verifications row in a single transaction.
    - Sends verification email with a signed token.
    """
    ic("Signup service triggered")

    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    ic(email, username)

    try:
        # Basic validation using shared validators
        email = validate_email(email)
        username = validate_username(username)
        password = validate_password(password)
    except ValidationError as ve:
        ic("Validation error", ve)
        return {
            "ok": False,
            "error": str(ve),
            # Keep values so the form can be repopulated
            "form": {
                "email": email,
                "username": username,
            },
        }

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        ic("Checking for duplicate email")
        cursor.execute(
            "SELECT user_id FROM users WHERE email = %s AND is_deleted = 0",
            (email,),
        )
        existing_email = cursor.fetchone()
        ic(existing_email)

        if existing_email:
            return {
                "ok": False,
                "error": "An account with this email already exists",
                "form": {
                    "email": email,
                    "username": username,
                },
            }

        ic("Checking for duplicate username")
        cursor.execute(
            "SELECT user_id FROM users WHERE username = %s AND is_deleted = 0",
            (username,),
        )
        existing_username = cursor.fetchone()
        ic(existing_username)

        if existing_username:
            return {
                "ok": False,
                "error": "This username is already taken",
                "form": {
                    "email": email,
                    "username": username,
                },
            }

        # Create user record with a secure password hash
        user_id = uuid.uuid4().hex
        ic("Generated user_id", user_id)
        password_hash = generate_password_hash(password)

        now = datetime.utcnow()
        epoch_now = now.timestamp()

        ic("Inserting new user into DB", epoch_now)
        cursor.execute(
            """
            INSERT INTO users (
              user_id, email, password_hash, username, display_name,
              bio, avatar_filename, is_admin, is_blocked, is_deleted,
              email_verified_at, created_at, updated_at
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                user_id,
                email,
                password_hash,
                username,
                None,
                None,
                None,
                0,
                0,
                0,
                None,
                epoch_now,
                epoch_now,
            ),
        )

        # Create verification token with expiry
        verification_id = uuid.uuid4().hex
        verification_token = uuid.uuid4().hex
        expires_at = epoch_now + VERIFICATION_TIME

        ic("Creating email_verification", verification_id, verification_token)
        ic(expires_at)
        cursor.execute(
            """
            INSERT INTO email_verifications (
              verification_id, user_id_fk, token, expires_at, verified_at, created_at
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                verification_id,
                user_id,
                verification_token,
                expires_at,
                None,
                epoch_now,
            ),
        )

        # Commit both user and verification in one transaction
        connection.commit()
        ic("User + email_verification committed")

        # Send verification email after commit to avoid dangling links
        send_verification_email(email, verification_token)

        return {
            "ok": True,
            "user_id": user_id,
        }

    except Exception as ex:
        ic("SIGNUP EXCEPTION", ex)
        if connection:
            connection.rollback()
        return {
            "ok": False,
            "error": "An unexpected error occurred. Please try again.",
        }

    finally:
        # Clean up DB resources
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def login():
    """
    Handles login:
    - Validates email format and ensures password is present.
    - Checks that the account exists, is not deleted/blocked, and email is verified.
    - Verifies password hash.
    - On success, sets session keys (user_id, username, is_admin).
    """
    ic("Login service er aktiveret")
    email = request.form.get("email")
    password = request.form.get("password")

    ic(email)

    try:
        email = validate_email(email)
    except ValidationError as ve:
        ic("fejl ved validation", ve)
        return {
            "ok": False,
            "error": str(ve),
            "form": {
                "email": email,
            },
        }

    if not password:
        return {
            "ok": False,
            "error": "Password is required",
            "form": {
                "email": email,
            },
        }

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        # Look up user by email
        cursor.execute(
            "SELECT * FROM users WHERE email = %s LIMIT 1",
            (email,),
        )

        user = cursor.fetchone()
        ic("Users Row", user)

        # Generic error message to avoid leaking whether the email exists
        if not user or user["is_deleted"]:
            return {
                "ok": False,
                "error": "Invalid email or password",
                "form": {
                    "email": email,
                },
            }

        if user["is_blocked"]:
            return {
                "ok": False,
                "error": "This account has been blocked by an administrator.",
                "form": {
                    "email": email,
                },
            }

        if user["email_verified_at"] is None:
            return {
                "ok": False,
                "error": "Your email is not verified. Please check your inbox.",
                "form": {
                    "email": email,
                },
            }

        # Verify password hash
        if not check_password_hash(user["password_hash"], password):
            return {
                "ok": False,
                "error": "Invalid email or password",
                "form": {
                    "email": email,
                },
            }

        # All checks passed: initialize session
        session.clear()
        session["user_id"] = user["user_id"]
        session["username"] = user["username"]
        session["is_admin"] = bool(user["is_admin"])

        ic("User logged in", user["user_id"], user["username"])

        return {
            "ok": True,
            "user_id": user["user_id"],
            "username": user["username"],
            "is_admin": bool(user["is_admin"]),
        }

    except Exception as ex:
        ic("LOGIN EXCEPTION", ex)
        return {
            "ok": False,
            "error": "An unexpected error occurred. Please try again.",
        }

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def request_password_reset():
    """
    Starts the password reset flow:
    - Validates email format.
    - If a valid, non-deleted, non-blocked user exists:
        - Creates a password_resets row with expiry.
        - Sends a reset email with a token.
    - Always returns ok=True on lookup errors to avoid account enumeration.
    """
    ic("reset password er aktivt")
    email = request.form.get("email")
    ic(email)

    try:
        email = validate_email(email)
    except ValidationError as ve:
        ic("Forgot password validation error", ve)
        return {
            "ok": False,
            "error": str(ve),
            "form": {"email": email},
        }

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT user_id, is_deleted, is_blocked
            FROM users
            WHERE email = %s
            LIMIT 1
            """,
            (email,),
        )

        user = cursor.fetchone()
        ic("User for the password resetting", user)

        # Security: even if user not found / invalid, return ok=True
        if not user or user["is_deleted"] or user["is_blocked"]:
            ic("No valid user for password reset, but returning ok for security")
            return {
                "ok": True,
            }

        user_id = user["user_id"]
        now = datetime.utcnow()
        epoch_now = now.timestamp()
        expires_at = epoch_now + RESET_PASSWORD_TIME
        reset_id = uuid.uuid4().hex
        reset_token = uuid.uuid4().hex

        ic("Making the password_reset", reset_id, reset_token, epoch_now)

        cursor.execute(
            """
            INSERT INTO password_resets (
              reset_id, user_id_fk, token, expires_at, used_at, created_at
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                reset_id,
                user_id,
                reset_token,
                expires_at,
                None,
                epoch_now,
            ),
        )
        connection.commit()

        # Send the email after committing the reset entry
        ic("Reset mail sent")
        send_password_reset_email(email, reset_token)

        return {"ok": True}

    except Exception as ex:
        ic("REQUEST PASSWORD RESET EXCEPTION", ex)
        if connection:
            connection.rollback()
        # Still return ok=True so we don't leak internal details
        return {"ok": True}

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def perform_password_reset(token: str):
    """
    Completes the password reset:
    - Validates that password and confirmation match and meet password requirements.
    - Looks up the reset token and checks:
        * Not used
        * Not expired
        * User is not deleted/blocked
    - Updates the user's password and marks the reset as used.
    """
    ic("perform reset trigged")

    new_password = request.form.get("password")
    confirm_new_password = request.form.get("confirm_new_password")

    if new_password != confirm_new_password:
        return {
            "ok": False,
            "error": "no password match",
        }

    try:
        new_password = validate_password(new_password)
    except ValidationError as ve:
        ic("password validation error", ve)
        return {
            "ok": False,
            "error": str(ve),
        }

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT pr.reset_id, pr.user_id_fk, pr.expires_at, pr.used_at, u.user_id, u.is_deleted, u.is_blocked
            FROM password_resets pr
            JOIN users u ON u.user_id = pr.user_id_fk
            WHERE pr.token = %s
            LIMIT 1
            """,
            (token,),
        )

        row = cursor.fetchone()
        ic("password resetting row", row)

        if not row:
            return {
                "ok": False,
                "error": "Invalid or expired password reset link.",
            }

        now = datetime.utcnow()
        epoch_now = now.timestamp()

        if row["used_at"] is not None:
            return {
                "ok": False,
                "error": "This password reset link has already been used.",
            }

        if row["expires_at"] is not None and epoch_now > row["expires_at"]:
            return {
                "ok": False,
                "error": "This password reset link has expired.",
            }

        if row["is_deleted"] or row["is_blocked"]:
            return {
                "ok": False,
                "error": "This account is not available.",
            }

        # Hash and store new password
        new_hash = generate_password_hash(new_password)
        ic("updating users password", row["user_id_fk"])

        cursor.execute(
            """
            UPDATE users
            SET password_hash = %s, updated_at = %s
            WHERE user_id = %s
            """,
            (new_hash, epoch_now, row["user_id_fk"]),
        )

        cursor.execute(
            """
            UPDATE password_resets
            SET used_at = %s
            WHERE reset_id = %s
            """,
            (epoch_now, row["reset_id"]),
        )

        connection.commit()
        ic("password is now updated!")

        return {"ok": True}

    except Exception as ex:
        ic("PERFORM PASSWORD RESET EXCEPTION", ex)
        if connection:
            connection.rollback()
        return {
            "ok": False,
            "error": "An unexpected error occurred. Please try again.",
        }

    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


def delete_account():
    """
    Deletes the currently logged-in user's account and related data.
    (Note: in this project, the active delete implementation is in user_service,
    but this function demonstrates a soft-delete strategy.)
    - Soft-deletes the user and their posts/comments.
    - Deletes likes and follow relationships.
    """
    user_id = session.get("user_id")

    ic("delete_account is now trigged", user_id)

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

        cursor.execute(
            "SELECT user_id, is_deleted FROM users WHERE user_id = %s LIMIT 1",
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

        # 4) Remove likes created by user
        cursor.execute(
            """
            DELETE FROM likes
            WHERE user_id_fk = %s
            """,
            (user_id,),
        )

        # 5) Remove follow relationships (both follower and followee)
        cursor.execute(
            """
            DELETE FROM follows
            WHERE follower_user_id_fk = %s OR followee_user_id_fk = %s
            """,
            (user_id, user_id),
        )

        connection.commit()
        ic("User and related data soft-deleted OK")

        return {
            "ok": True,
        }

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
