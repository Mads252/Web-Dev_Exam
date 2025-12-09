from flask import Blueprint, render_template, redirect, url_for, session
from services.user_service import (
    get_user_by_username,
    get_current_user,
    update_profile_and_avatar,
    is_following,
    get_follow_stats,
    delete_current_user,
)
from debug import ic


# Blueprint that groups all user/profile related routes
user_routes = Blueprint("user_routes", __name__)


@user_routes.get("/profile/<username>")
def profile_view(username):
    """
    Public profile page.
    - Visible to everyone.
    - Shows follower/following counts.
    - Shows follow/unfollow button for logged-in users.
    """
    ic("GET /profile", username)

    profile_user = get_user_by_username(username)
    if not profile_user:
        return "User not found", 404

    current_user = get_current_user()

    # Fetch follower / following counts for the profile user
    follow_stats = get_follow_stats(profile_user["user_id"])

    # Determine whether the current user is already following this profile
    currently_following = False
    if current_user:
        currently_following = is_following(
            current_user["user_id"],
            profile_user["user_id"],
        )

    return render_template(
        "profile.html",
        profile_user=profile_user,
        current_user=current_user,
        follow_stats=follow_stats,
        currently_following=currently_following,
    )


@user_routes.get("/settings/profile")
def profile_settings_get():
    """
    Shows the profile settings page for the logged-in user.
    Allows editing display name, bio, and avatar.
    """
    ic("GET /settings/profile")

    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    current_user = get_current_user()
    if not current_user:
        return redirect(url_for("auth_routes.login_get"))

    return render_template("settings_profile.html", user=current_user)


@user_routes.post("/settings/profile")
def profile_settings_post():
    """
    Handles profile update submissions.
    Delegates validation and file handling to user_service.update_profile_and_avatar.
    """
    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    result = update_profile_and_avatar()
    ic(result)

    if not result["ok"]:
        # On validation error: re-render form with current user and submitted values
        current_user = get_current_user()
        return render_template(
            "settings_profile.html",
            user=current_user,
            error=result.get("error"),
            form=result.get("form", {}),
        ), 400

    ic("Profile updated")
    # Redirect back to the settings page to avoid form resubmission
    return redirect(url_for("user_routes.profile_settings_get"))


@user_routes.get("/settings/delete-account")
def delete_account_get():
    """
    Shows the delete account confirmation page for the logged-in user.
    """
    ic("GET /settings/delete-account")

    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    current_user = get_current_user()
    if not current_user:
        return redirect(url_for("auth_routes.login_get"))

    return render_template("delete_account.html", user=current_user)


@user_routes.post("/settings/delete-account")
def delete_account_post():
    """
    Handles account deletion.
    - Delegates delete logic to user_service.delete_current_user.
    - On success, clears the session and redirects to login.
    """
    ic("POST /settings/delete-account")

    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    result = delete_current_user()
    ic(result)

    # If deletion succeeded, log the user out and redirect to login
    if result.get("ok"):
        session.clear()
        return redirect(url_for("auth_routes.login_get"))

    # If something went wrong, show the confirmation page again with an error message
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for("auth_routes.login_get"))

    return render_template(
        "delete_account.html",
        user=current_user,
        error=result.get("error"),
    ), 400
