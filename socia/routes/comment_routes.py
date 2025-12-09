from flask import Blueprint, redirect, url_for, request, session, render_template
from services.user_service import get_current_user
from services.comment_service import create_comment, delete_comment, get_comments_for_post
from debug import ic

# Blueprint for all comment-related routes (classic + MixHTML API)
comment_routes = Blueprint("comment_routes", __name__)


@comment_routes.post("/posts/<post_id>/comments")
def create_comment_post(post_id):
    ic("POST /posts/<post_id>/comments", post_id)

    # Only logged-in users can create comments
    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    result = create_comment(post_id)
    ic(result)

    # Simple post/redirect pattern: go back to where the request came from
    referer = request.headers.get("Referer")
    if referer:
        return redirect(referer)

    return redirect(url_for("post_routes.home"))


@comment_routes.post("/comments/<comment_id>/delete")
def delete_comment_route(comment_id):
    ic("POST /comments/<comment_id>/delete", comment_id)

    # Protect delete action behind login
    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    result = delete_comment(comment_id)
    ic(result)

    # Redirect back to previous page (e.g. home feed or profile)
    referer = request.headers.get("Referer")
    if referer:
        return redirect(referer)

    return redirect(url_for("post_routes.home"))


@comment_routes.post("/api/posts/<post_id>/comments")
def api_create_comment_mix(post_id):
    """
    MixHTML API endpoint for creating a comment.
    - Returns <mixhtml> snippets instead of a full page.
    - On success, re-renders only the comments block for the post.
    - On error, shows a toast message.
    """
    try:
        ic("POST /api/posts/<post_id>/comments", post_id)

        # Unauthenticated users get a MixHTML redirect to the login page
        if not session.get("user_id"):
            login_url = url_for("auth_routes.login_get")
            return f'<mixhtml mix-redirect="{login_url}"></mixhtml>', 401

        # Business logic is handled by the comment_service
        result = create_comment(post_id)
        ic(result)

        # Validation errors are shown as a toast at the bottom of the page
        if not result.get("ok"):
            error_msg = result.get("error", "Error creating comment")
            toast_html = render_template("partials/toasts/error.html", message=error_msg)
            return f'<mixhtml mix-bottom="#toast">{toast_html}</mixhtml>', 400

        # On success: reload the comments for this post and update that block only
        current_user = get_current_user()
        comments = get_comments_for_post(post_id)

        comments_html = render_template(
            "partials/home/post_comments_block.html",
            post_id=post_id,
            comments=comments,
            current_user=current_user,
        )

        return (
            f'<mixhtml mix-update="#post-{post_id}-comments">{comments_html}</mixhtml>',
            200,
        )

    except Exception as ex:
        # Generic system error, shown as toast; details logged via ic
        ic(ex)
        toast_html = render_template("partials/toasts/error.html", message="System error")
        return f'<mixhtml mix-bottom="#toast">{toast_html}</mixhtml>', 500
