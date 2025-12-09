# validators.py
import re
import uuid
import os


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,20}$")

def validate_email(email: str) -> str:
    if not email:
        raise ValidationError("Email is required")
    email = email.strip().lower()
    if not EMAIL_REGEX.match(email):
        raise ValidationError("Invalid email format")
    return email

def validate_username(username: str) -> str:
    if not username:
        raise ValidationError("Username is required")
    username = username.strip()
    if not USERNAME_REGEX.match(username):
        raise ValidationError("Username must be 3-20 characters and only contain letters, numbers and underscore")
    return username

def validate_password(password: str) -> str:
    if not password:
        raise ValidationError("Password is required")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters")
    # du kan udvide her med tal/specialtegn osv.
    return password

def validate_uuid(id_str: str) -> str:
    if not id_str:
        raise ValidationError("ID is required")
    if len(id_str) != 32:
        raise ValidationError("Invalid id format")
    # simple check – du kan også prøve at parse som UUID
    return id_str


# validators.py (fortsættelse)

def validate_display_name(display_name: str | None) -> str | None:
    if display_name is None:
        return None
    display_name = display_name.strip()
    if not display_name:
        return None
    if len(display_name) > 100:
        raise ValidationError("Display name must be at most 100 characters")
    return display_name


def validate_bio(bio: str | None) -> str | None:
    if bio is None:
        return None
    bio = bio.strip()
    if not bio:
        return None
    if len(bio) > 160:
        raise ValidationError("Bio must be at most 160 characters")
    return bio


ALLOWED_AVATAR_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
ALLOWED_AVATAR_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

def validate_avatar_file(file_storage) -> None:
 
    if not file_storage:
        raise ValidationError("No file uploaded")

    filename = file_storage.filename
    if not filename:
        raise ValidationError("No file selected")

    _, ext = os.path.splitext(filename.lower())
    if ext not in ALLOWED_AVATAR_EXTENSIONS:
        raise ValidationError("Avatar must be a JPG, PNG or GIF file")

    mimetype = file_storage.mimetype
    if mimetype not in ALLOWED_AVATAR_MIMETYPES:
        raise ValidationError("Invalid image format")



def validate_post_content(content: str | None) -> str | None:
    """
    Validerer post-tekst.
    Tillader tom, MEN så skal der være mindst ét billede (tjekker vi i service).
    """
    if content is None:
        return None
    content = content.strip()
    if not content:
        return None
    if len(content) > 280:
        raise ValidationError("Post content must be at most 280 characters")
    return content


ALLOWED_POST_MEDIA_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
ALLOWED_POST_MEDIA_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

def validate_post_media_file(file_storage) -> None:
    """
    Validerer ét uploadet post-mediefil.
    """
    if not file_storage:
        raise ValidationError("No file uploaded")

    filename = file_storage.filename
    if not filename:
        raise ValidationError("No file selected")

    _, ext = os.path.splitext(filename.lower())
    if ext not in ALLOWED_POST_MEDIA_EXTENSIONS:
        raise ValidationError("Media files must be JPG, PNG or GIF")

    mimetype = file_storage.mimetype
    if mimetype not in ALLOWED_POST_MEDIA_MIMETYPES:
        raise ValidationError("Invalid media file format")


def validate_comment_content(content: str | None) -> str:
    if content is None:
        raise ValidationError("Comment is required")
    content = content.strip()
    if not content:
        raise ValidationError("Comment cannot be empty")
    if len(content) > 280:
        raise ValidationError("Comment must be at most 280 characters")
    return content
