# app.py
import os
from flask import Flask, render_template
from flask_session import Session
from routes.auth_routes import auth_routes
from debug import ic
from routes.post_routes import post_routes

from routes.user_routes import user_routes

from routes.like_routes import like_routes

from routes.comment_routes import comment_routes

from routes.follow_routes import follow_routes

from routes.admin_routes import admin_routes

from services.i18n_service import load_dictionary, t, get_current_language

from routes.language_routes import language_routes

from routes.search_routes import search_routes

app = Flask(__name__)
app.config["SECRET_KEY"] = "skift_mig_senere"  # eller fra .env


def create_app():
    app = Flask(__name__)

    # SECRET_KEY + session config
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = False
    #avatar-safe
    app.config["AVATAR_UPLOAD_FOLDER"] = "static/uploads/avatars"

    #post-save
    app.config["POST_UPLOAD_FOLDER"] = "static/uploads/posts"

    #translation
    app.config["TRANSLATION_FILE"] = "dictionary.json"
    app.config["LANGUAGES"] = [
    "english",
    "amharic",
    "arabic",
    "basque",
    "bengali",
    "english (uk)",
    "portuguese (brazil)",
    "bulgarian",
    "catalan",
    "cherokee",
    "croatian",
    "czech",
    "danish",
    "dutch",
    "english (us)",
    "estonian",
    "filipino",
    "finnish",
    "french",
    "german",
    "greek",
    "gujarati",
    "hebrew",
    "hindi",
    "hungarian",
    "icelandic",
    "indonesian",
    "italian",
    "japanese",
    "kannada",
    "korean",
    "latvian",
    "lithuanian",
    "malay",
    "malayalam",
    "marathi",
    "norwegian",
    "polish",
    "portuguese (portugal)",
    "romanian",
    "russian",
    "serbian",
    "chinese (prc)",
    "slovak",
    "slovenian",
    "spanish",
    "swahili",
    "swedish",
    "tamil",
    "telugu",
    "thai",
    "chinese (taiwan)",
    "turkish",
    "urdu",
    "ukrainian",
    "vietnamese",
    "welsh"
]

    app.config["LANG_DEFAULT"] = "english"

    
    Session(app)  #Aktivering af flask sessionen

    
    app.register_blueprint(auth_routes)
    app.register_blueprint(post_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(like_routes)
    app.register_blueprint(comment_routes)
    app.register_blueprint(follow_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(language_routes)
    app.register_blueprint(search_routes)

    return app

app = create_app()



##############################
##############################
##############################



def setup_dictionary():
    load_dictionary()

with app.app_context():
    setup_dictionary()

@app.context_processor
def inject_i18n():
    return {
        "t": t,
        "current_language": get_current_language(),
        "available_languages": app.config.get("LANGUAGES", []),
    }
