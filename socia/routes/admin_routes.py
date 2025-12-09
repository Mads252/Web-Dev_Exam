from flask import Blueprint, render_template, redirect, url_for, session, request, current_app
from services.admin_service import get_all_users, get_recent_posts, toggle_user_block, toggle_post_block
from debug import ic
import os
import csv
import io
import json
import requests

# admin_routes blueprint groups all admin-only endpoints
admin_routes = Blueprint("admin_routes", __name__)


def _require_admin():
    """
    Small guard helper used by all admin routes.
    - Redirects to login if no user is in the session.
    - Returns 403 if the logged-in user is not an admin.
    """
    if not session.get("user_id"):
        return redirect(url_for("auth_routes.login_get"))

    if not session.get("is_admin"):
        return "Forbidden: admin access required", 403

    return None


@admin_routes.get("/admin")
def admin_dashboard():
    # All admin pages call the shared guard at the top
    guard = _require_admin()
    if guard:
        return guard

    return render_template("admin/dashboard.html")


@admin_routes.get("/admin/users")
def admin_users():
    guard = _require_admin()
    if guard:
        return guard

    # Data access is delegated to the admin_service layer
    users = get_all_users()
    return render_template("admin/admin_users.html", users=users)


@admin_routes.post("/admin/users/<user_id>/toggle-block")
def admin_toggle_user_block(user_id):
    ic("POST /admin/users/<user_id>/toggle-block", user_id)

    guard = _require_admin()
    if guard:
        return guard

    # Service call encapsulates the logic of block/unblock + side effects (emails, etc.)
    result = toggle_user_block(user_id)
    ic(result)

    # Redirect back to the page the admin came from (users or other filtered view)
    referer = request.headers.get("Referer")
    if referer:
        return redirect(referer)

    return redirect(url_for("admin_routes.admin_users"))


@admin_routes.get("/admin/posts")
def admin_posts():
    ic("GET /admin/posts")
    guard = _require_admin()
    if guard:
        return guard

    # Limit for safety and performance in the admin table
    posts = get_recent_posts(limit=50)
    return render_template("admin/admin_posts.html", posts=posts)


@admin_routes.post("/admin/posts/<post_id>/toggle-block")
def admin_toggle_post_block(post_id):
    ic("POST /admin/posts/<post_id>/toggle-block", post_id)

    guard = _require_admin()
    if guard:
        return guard

    result = toggle_post_block(post_id)
    ic(result)

    # Same referer pattern as for users: admin is sent back to where they were
    referer = request.headers.get("Referer")
    if referer:
        return redirect(referer)

    return redirect(url_for("admin_routes.admin_posts"))


@admin_routes.get("/get-data-from-sheet")
def get_data_from_sheet():
    """
    Admin-only endpoint that pulls translation data from a Google Sheet (CSV export),
    converts it into a nested JSON structure and writes it to the dictionary file
    configured in Flask's app.config. Finally it reloads the in-memory dictionary.
    """
    try:
        ic("GET /get-data-from-sheet")

        guard = _require_admin()
        if guard:
            return guard  # Only admins can update translations

        # Spreadsheet key is currently hard-coded; could be moved to environment/config
        excelkey = os.getenv("google_spread_sheet_key")
        url = (
            f"https://docs.google.com/spreadsheets/d/"
            f"{excelkey}/export?format=csv&id={excelkey}"
        )

        # Download the sheet as CSV
        res = requests.get(url=url)
        csv_text = res.content.decode("utf-8")
        csv_file = io.StringIO(csv_text)

        # DictReader lets us access each column by header name
        reader = csv.DictReader(csv_file)

        # LANGUAGES config defines which language columns we expect in the sheet
        languages = current_app.config.get("LANGUAGES", [])

        data = {}

        for row in reader:
            # Build a per-key dict of all translations from the configured languages
            item = {}
            for lang in languages:
                # row.get avoids KeyError if a column is missing
                item[lang] = row.get(lang, "")

            # "key" column identifies the translation key in the sheet
            key = row.get("key")
            if key:
                data[key] = item

        # Write the translation dictionary as pretty-printed UTF-8 JSON
        json_data = json.dumps(data, ensure_ascii=False, indent=4)

        dict_path = current_app.config.get("TRANSLATION_FILE", "dictionary.json")
        ic("Writing dictionary to", dict_path)

        with open(dict_path, "w", encoding="utf-8") as f:
            f.write(json_data)

        # Reload the in-memory translation dictionary so changes take effect immediately
        from services.i18n_service import load_dictionary
        load_dictionary()
        ic("Translation dictionary reloaded")

        return redirect(url_for("admin_routes.admin_dashboard"))

    except Exception as ex:
        # Debug output only; in production this could be replaced with proper logging
        ic(ex)
        return str(ex)
    finally:
        pass
