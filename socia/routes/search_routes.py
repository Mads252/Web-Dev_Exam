# routes/search_routes.py
from flask import Blueprint, request, jsonify
from debug import ic
from db import db

# Blueprint grouping all search-related API endpoints
search_routes = Blueprint("search_routes", __name__)


@search_routes.post("/api/search-users")
def api_search_users():
    """
    Lightweight search endpoint used by the search bar (AJAX/MixHTML-free).
    Returns a JSON list with matching users based on username or display_name.
    - Uses SQL placeholders to prevent injection.
    - Always limits results for performance (max 10 results).
    """
    try:
        ic("POST /api/search-users")

        # Extract search query from form data and sanitize it
        search_for = request.form.get("search_for", "")
        search_for = (search_for or "").strip()
        ic("search_for", search_for)

        if not search_for:
            # Client-side ensures this rarely happens, but we validate anyway
            return "empty search", 400

        # "LIKE %term%" pattern to match anywhere in username or display_name
        part_of_query = f"%{search_for}%"

        connection = None
        cursor = None

        connection = db()
        cursor = connection.cursor(dictionary=True)

        # Query for matching users; excludes deleted accounts
        cursor.execute(
            """
            SELECT
              user_id,
              username,
              display_name,
              avatar_filename
            FROM users
            WHERE is_deleted = 0
              AND (
                username LIKE %s
                OR display_name LIKE %s
              )
            ORDER BY username ASC
            LIMIT 10
            """,
            (part_of_query, part_of_query),
        )

        users = cursor.fetchall() or []
        ic("search results", len(users))

        # Return JSON directly to be parsed in search.js
        return jsonify(users), 200

    except Exception as ex:
        # Log internal exception for debugging
        ic("api_search_users EXCEPTION", ex)
        return str(ex), 500

    finally:
        # Clean up DB resources safely
        if "cursor" in locals() and cursor:
            cursor.close()
        if "connection" in locals() and connection:
            connection.close()
