from flask import Blueprint, redirect, request, url_for
from services.i18n_service import set_current_language
from debug import ic

# Blueprint responsible for switching UI language at runtime
language_routes = Blueprint("language_routes", __name__)


@language_routes.get("/set-language/<lang_code>")
def set_language_route(lang_code):
    """
    Sets the user's preferred UI language.
    The preference is stored (typically in session) by i18n_service.
    After updating the language, the user is redirected back to the page they came from.
    """
    ic("set_language_route", lang_code)

    # Update the active language using the central i18n service
    set_current_language(lang_code)

    # Redirect the user back to the previous view for seamless UX
    referer = request.headers.get("Referer")
    if referer:
        return redirect(referer)

    # Fallback: send user to the feed
    return redirect(url_for("post_routes.home"))
