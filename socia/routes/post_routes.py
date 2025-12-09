# routes/post_routes.py
from flask import Blueprint, render_template, redirect, url_for, session, request
from services.post_service import (
    create_post,
    get_latest_posts,
    get_post_by_id,
    update_post,
    delete_post,
    get_latest_posts_from_following,
)
from services.user_service import get_current_user
from debug import ic

# Blueprint that groups all public feed and post-related routes
post_routes = Blueprint("post_routes", __name__)


@post_routes.get("/")
def home():
    """
    Home feed.
    - If `feed=following` and user is logged in → show posts from followed users.
    - Otherwise → show global feed with latest posts.
    """
    ic("GET / (home)")

    current_user = get_current_user()
    current_user_id = current_user["user_id"] if current_user else None

    feed = request.args.get("feed", "all")
    ic("feed type", feed)

    if feed == "following" and current_user_id:
        # Personalized feed: only posts from accounts the user follows
        posts = get_latest_posts_from_following(
            follower_user_id=current_user_id,
            limit=20,
        )
    else:
        # Default: global feed
        # Ensure template always receives either 'all' or 'following'
        feed = "all"
        posts = get_latest_posts(limit=20, current_user_id=current_user_id)

    return render_template(
        "home.html",
        current_user=current_user,
        posts=posts,
        feed=feed,
    )


@post_routes.post("/posts")
def create_post_route():
    """
    Classic POST endpoint for creating a new post (non-MixHTML).
    Uses the same service as the MixHTML API version.
    """
    ic("POST /posts (create_post_route)")

    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    result = create_post()
    ic(result)

    if not result["ok"]:
        # On validation error: re-render home with error message + original content
        current_user = get_current_user()
        posts = get_latest_posts(limit=20)
        return render_template(
            "home.html",
            current_user=current_user,
            posts=posts,
            error=result.get("error"),
            form=result.get("form", {}),
        ), 400

    return redirect(url_for("post_routes.home"))


@post_routes.get("/posts/<post_id>/edit")
def edit_post_get(post_id):
    """
    Show edit form for a specific post.
    Only the post owner or an admin is allowed to access this page.
    """
    ic("GET /posts/<post_id>/edit", post_id)

    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    post = get_post_by_id(post_id)
    if not post or post["is_deleted"]:
        return "Post not found", 404

    current_user = get_current_user()
    if not current_user:
        return redirect(url_for("auth_routes.login_get"))

    # Permission check: only owner or admin may edit
    if post["user_id_fk"] != current_user["user_id"] and not current_user["is_admin"]:
        return "You are not allowed to edit this post", 403

    return render_template("edit_post.html", post=post)


@post_routes.post("/posts/<post_id>/edit")
def edit_post_post(post_id):
    """
    Handles the form submission for editing a post.
    """
    ic("POST /posts/<post_id>/edit", post_id)

    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    result = update_post(post_id)
    ic(result)

    if not result["ok"]:
        post = get_post_by_id(post_id)
        if not post:
            return "Post not found", 404

        # Re-render edit page with validation error
        return render_template(
            "edit_post.html",
            post=post,
            error=result.get("error"),
        ), 400

    # Redirect back to home (could later be a dedicated single-post view)
    return redirect(url_for("post_routes.home"))


@post_routes.post("/posts/<post_id>/delete")
def delete_post_route(post_id):
    """
    Soft-deletes a post via the service layer.
    Only accessible for logged-in users; further checks are done in the service.
    """
    ic("POST /posts/<post_id>/delete", post_id)

    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    result = delete_post(post_id)
    ic(result)

    # Regardless of result, return to the home feed
    return redirect(url_for("post_routes.home"))


@post_routes.post("/api/posts")
def api_create_post_mix():
    """
    MixHTML endpoint for creating a new post.
    - On success: renders the newest post as HTML and inserts it at the top of the feed.
    - On validation error: shows a toast with the error message.
    """
    try:
        ic("POST /api/posts (mix create)")

        if not session.get("user_id"):
            login_url = url_for("auth_routes.login_get")
            # MixHTML redirect for unauthenticated users
            return f'<mixhtml mix-redirect="{login_url}"></mixhtml>', 401

        # Reuse the same service as the normal /posts endpoint
        result = create_post()
        ic(result)

        if not result.get("ok"):
            error_msg = result.get("error", "Error creating post")
            toast_html = render_template(
                "partials/mix/toast_error.html",
                error=error_msg,
            )
            # Show error toast at the bottom of the page
            return f'<mixhtml mix-bottom="#toast">{toast_html}</mixhtml>', 400

        post_id = result.get("post_id")
        current_user = get_current_user()
        current_user_id = current_user["user_id"] if current_user else None

        # Simple trick: fetch the latest post (limit=1) for this user context
        items = get_latest_posts(limit=1, current_user_id=current_user_id)
        if not items:
            toast_html = render_template(
                "partials/mix/toast_error.html",
                error="Could not load new post",
            )
            return f'<mixhtml mix-bottom="#toast">{toast_html}</mixhtml>', 500

        item = items[0]

        # Render the single post item partial
        post_html = render_template(
            "partials/home/post_item.html",
            item=item,
            current_user=current_user,
        )

        toast_confirm = render_template(
            "partials/mix/toast_ok.html",
            message="New post created!",
        )

        # MixHTML:
        # - mix-top inserts the new post at the top of the feed list
        # - mix-bottom appends a confirmation toast to the toast container
        return (
            f"""<mixhtml mix-top="#feed">{post_html}</mixhtml>
        <mixhtml mix-bottom="#toast">{toast_confirm}</mixhtml>""",
            200,
        )

    except Exception as ex:
        # Fallback: generic system error toast
        ic(ex)
        toast_html = render_template(
            "partials/mix/toast_error.html",
            error="System error",
        )
        return f'<mixhtml mix-bottom="#toast">{toast_html}</mixhtml>', 500
