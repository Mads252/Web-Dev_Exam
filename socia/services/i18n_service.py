import json
from flask import current_app, session
from debug import ic

# In-memory cache of the translation dictionary.
# Structure: { "key": { "english": "...", "danish": "...", ... } }
_dictionary: dict[str, dict[str, str]] = {}


def load_dictionary():
    """
    Load the dictionary.json file into memory.
    Called once at app startup and again when the admin reloads translations
    from the Google Sheet.
    """
    global _dictionary
    path = current_app.config.get("TRANSLATION_FILE", "dictionary.json")
    ic("Loading dictionary from", path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            _dictionary = json.load(f)
            ic("Dictionary loaded with keys:", list(_dictionary.keys()))
    except Exception as ex:
        # If file missing or corrupted, fallback to empty dict (safe fail)
        ic("LOAD_DICTIONARY_EXCEPTION", ex)
        _dictionary = {}


def get_current_language() -> str:
    """
    Returns the current language selected by the user.
    Stored in session; falls back to the app’s default language.
    """
    lang = session.get("language")
    if not lang:
        lang = current_app.config.get("LANG_DEFAULT", "english")
    return lang


def set_current_language(lang: str):
    """
    Updates the user's chosen language if it is allowed.
    Language names must match column names used in dictionary.json
    (e.g. english, danish, spanish).
    """
    allowed = current_app.config.get("LANGUAGES", ["english"])
    ic("set_current_language", lang, allowed)

    if lang in allowed:
        session["language"] = lang


def t(key: str) -> str:
    """
    Translation lookup function.
    - Tries to return the text for the current language.
    - Falls back to English if available.
    - Falls back to the key itself if no translation exists.
    
    This ensures templates never crash due to missing translations.
    """
    lang = get_current_language()

    entry = _dictionary.get(key)
    if not entry:
        return key 

    text = entry.get(lang)
    if text:
        return text

    # Fallback to English if translation missing
    if lang != "english" and "english" in entry:
        return entry["english"]

    # Final fallback: return the key so UI stays readable
    return key
