from flask import Blueprint, redirect, url_for, request, session
from services.follow_service import toggle_follow_by_username
from debug import ic

# Blueprint that groups all follow/unfollow related routes
follow_routes = Blueprint("follow_routes", __name__)


@follow_routes.post("/users/<username>/follow")
def follow_toggle_route(username):
    """
    Toggles follow/unfollow for the given username.
    The actual logic (including checks and constraints) lives in follow_service.
    """
    ic("POST /users/<username>/follow", username)

    # Only logged-in users can follow or unfollow
    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    # Delegate follow/unfollow logic to the service layer
    result = toggle_follow_by_username(username)
    ic(result)

    # Redirect back to where the request came from (e.g. profile or home feed)
    referer = request.headers.get("Referer")
    if referer:
        return redirect(referer)

    # Fallback: go to the profile page of the user that was followed/unfollowed
    return redirect(url_for("user_routes.profile_view", username=username))
