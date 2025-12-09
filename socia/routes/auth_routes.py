from flask import Blueprint, render_template, redirect, url_for, session
from services.auth_service import (
    signup as signup_service,
    login as login_service,
    request_password_reset,
    perform_password_reset,
)
from db import db
from debug import ic
from datetime import datetime

# Blueprint that groups all authentication-related routes
auth_routes = Blueprint("auth_routes", __name__)


@auth_routes.get("/signup")
def signup_get():
    # Simple GET endpoint: shows the sign-up form
    return render_template("signup.html")


@auth_routes.post("/signup")
def signup_post():
    ic("POST /signup triggered")

    # Delegate actual validation + user creation to the auth_service
    result = signup_service()
    ic(result)

    if not result["ok"]:
        # Re-render form with error message and previously entered values
        return render_template(
            "signup.html",
            error=result["error"],
            form=result.get("form"),
        ), 400

    # On success we show the “check your email” notice
    return redirect(url_for("auth_routes.verify_notice"))


@auth_routes.get("/verify-notice")
def verify_notice():
    # Shown right after signup, before the user clicks the email verification link
    return render_template("verify_notice.html")


@auth_routes.get("/verify/<token>")
def verify_email(token):
    """
    Handles email verification links.
    - Looks up the token in the email_verifications table.
    - Checks expiration and already-verified status.
    - Marks the user and the verification row as verified in a single transaction.
    """
    ic("verify_email called with token", token)

    connection = None
    cursor = None

    try:
        connection = db()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                ev.verification_id,
                ev.user_id_fk,
                ev.expires_at,
                ev.verified_at,
                u.user_id,
                u.email_verified_at
            FROM email_verifications ev
            JOIN users u ON u.user_id = ev.user_id_fk
            WHERE ev.token = %s
            """,
            (token,),
        )

        row = cursor.fetchone()
        ic("Verification row", row)

        if not row:
            # Invalid token: show error state
            return render_template(
                "partials/emails/verify_result.html",
                status="error",
                message="Invalid verification link",
            ), 400

        now = datetime.utcnow()
        epoch_now = now.timestamp()

        # Already verified? Show success, but do not update again
        if row["verified_at"] is not None or row["email_verified_at"] is not None:
            return render_template(
                "partials/emails/verify_result.html",
                status="ok",
                message="Your email is already verified. You can log in.",
            )

        # Check expiration timestamp
        if row["expires_at"] is not None and epoch_now > row["expires_at"]:
            return render_template(
                "partials/emails/verify_result.html",
                status="error",
                message=(
                    "This verification link has expired. "
                    "Please sign up again or request a new verification email."
                ),
            ), 400

        # Mark user and verification row as verified in the same transaction
        cursor.execute(
            "UPDATE users SET email_verified_at = %s, updated_at = %s WHERE user_id = %s",
            (epoch_now, epoch_now, row["user_id_fk"]),
        )

        cursor.execute(
            "UPDATE email_verifications SET verified_at = %s WHERE verification_id = %s",
            (epoch_now, row["verification_id"]),
        )

        connection.commit()
        ic("Email verification successful")

        return render_template(
            "partials/emails/verify_result.html",
            status="ok",
            message="Your email has been verified. You can now log in.",
        )

    except Exception as ex:
        # Roll back the transaction on any unexpected error
        ic("VERIFY EMAIL EXCEPTION", ex)
        if connection:
            connection.rollback()
        return render_template(
            "partials/emails/verify_result.html",
            status="error",
            message="An unexpected error occurred during verification.",
        ), 500

    finally:
        # Always clean up DB resources
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            pass


@auth_routes.get("/login")
def login_get():
    # If already logged in, skip the login page
    if session.get("user_id"):
        return redirect("/")
    return render_template("login.html")


@auth_routes.post("/login")
def login_post():
    ic("POST /login triggered")

    # Actual authentication logic lives in auth_service.login
    result = login_service()
    ic(result)

    if not result["ok"]:
        # Show login again with error message and submitted email
        return render_template(
            "login.html",
            error=result.get("error"),
            form=result.get("form", {}),
        ), 400

    # On success redirect to the home feed
    return redirect(url_for("post_routes.home"))


@auth_routes.get("/logout")
def logout_get():
    ic("User logged out")
    # Clear entire session to remove user_id, is_admin, language, etc.
    session.clear()
    return redirect("/login")


@auth_routes.get("/forgot-password")
def forgot_password_get():
    # Shows the "request password reset" form
    return render_template("partials/password/forgot_password.html")


@auth_routes.post("/forgot-password")
def forgot_password_post():
    ic("POST /forgot-password triggered")

    # Service handles lookup and sending the reset email
    result = request_password_reset()
    ic(result)

    if not result["ok"]:
        # Same view with error + preserved form data
        return render_template(
            "partials/password/forgot_password.html",
            error=result.get("error"),
            form=result.get("form", {}),
        ), 400

    # Always redirect to a generic notice (no user enumeration)
    return redirect(url_for("auth_routes.forgot_password_notice"))


@auth_routes.get("/forgot-password-notice")
def forgot_password_notice():
    # Generic message: "If an account exists, we have sent an email"
    return render_template("partials/password/forgot_password_notice.html")


@auth_routes.get("/reset-password/<token>")
def reset_password_get(token):
    ic("GET /reset-password with token", token)

    # Show the "choose new password" form with the token in the URL
    return render_template("partials/password/reset_password.html", token=token)


@auth_routes.post("/reset-password/<token>")
def reset_password_post(token):
    ic("POST /reset-password with token", token)

    # Service validates token, checks expiry and updates the password
    result = perform_password_reset(token)
    ic(result)

    if not result["ok"]:
        # Re-render form with error message (invalid token, weak password, etc.)
        return render_template(
            "partials/password/reset_password.html",
            token=token,
            error=result.get("error"),
        ), 400

    # On success show a small result page instead of auto-login
    return render_template(
        "partials/password/reset_password_result.html",
        status="ok",
        message="Your password has been updated. You can now log in.",
    )
