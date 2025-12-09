from flask import Blueprint, redirect, url_for, request, session, render_template
from services.like_service import toggle_like
from services.post_service import get_like_state_for_post
from services.user_service import get_current_user
from debug import ic

# Blueprint grouping all like/unlike related endpoints (classic + MixHTML)
like_routes = Blueprint("like_routes", __name__)


@like_routes.post("/mix/posts/<post_id>/like")
def like_toggle_mix_route(post_id):
    """
    AJAX/MixHTML like/unlike endpoint.
    - Requires authenticated user.
    - Toggles the like in the database via service layer.
    - Re-renders only the like block instead of the whole page.
    - Also shows a small toast notification (liked/unliked).
    """
    ic("POST /mix/posts/<post_id>/like", post_id)

    # If user is not logged in → redirect using MixHTML so the browser navigates.
    if not session.get("user_id"):
        login_url = url_for("auth_routes.login_get")
        return f'<mixhtml mix-redirect="{login_url}"></mixhtml>'

    # Business logic: toggle like for this post
    result = toggle_like(post_id)
    ic(result)

    # Determine the new like state (count + whether current user liked it)
    current_user = get_current_user()
    current_user_id = current_user["user_id"] if current_user else None

    state = get_like_state_for_post(post_id, current_user_id)
    ic("Like state after toggle", state)

    # Create a toast message depending on action
    if state["liked_by_current_user"]:
        toast = render_template(
            "partials/mix/toast_ok.html",
            message="You liked this post!"
        )
    else:
        toast = render_template(
            "partials/mix/toast_ok.html",
            message="You unliked this post!"
        )

    # Render updated like block so only that area refreshes
    like_block = render_template(
        "partials/mix/like_update.html",
        post_id=post_id,
        like_count=state["like_count"],
        liked_by_current_user=state["liked_by_current_user"],
        current_user=current_user,
    )

    # Return MixHTML response:
    # - <browser mix-bottom> shows the toast
    # - like_block updates the like UI
    return f"""
        <browser mix-bottom="#toast">{toast}</browser>
        {like_block}
    """




###################################
###################################
###################################
###################################
###################################

# slet dette hvis alt stadig virker

""" 

@like_routes.post("/posts/<post_id>/like")
def like_toggle_route(post_id):
  ic("POST /posts/<post_id>/like", post_id)

  if not session.get("user_id"):
      return redirect(url_for("auth_routes.login_get"))

  result = toggle_like(post_id)
  ic(result)

# MIXHTML / AJAX-MODE: hvis kaldet via fetch/XHR → returner kun HTML-snippet
  if request.headers.get("X-Requested-With") == "XMLHttpRequest":
      current_user = get_current_user()
      current_user_id = current_user["user_id"] if current_user else None

      state = get_like_state_for_post(post_id, current_user_id)
      ic("Like state after toggle", state)

      return render_template(
          "partials/home/post_like_block.html",
          post_id=post_id,
          like_count=state["like_count"],
          liked_by_current_user=state["liked_by_current_user"],
          current_user=current_user,
      )
  # NORMAL MODE (no JS): redirect tilbage
  referer = request.headers.get("Referer")
  if referer:
      return redirect(referer)

  return redirect(url_for("post_routes.home"))
 """