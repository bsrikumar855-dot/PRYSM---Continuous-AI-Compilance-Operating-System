"""Input validators."""

from app.config.constants import SUPPORTED_FILE_EXTENSIONS


def is_supported_file(filename: str) -> bool:
    import os
    ext = os.path.splitext(filename)[1].lower()
    return ext in SUPPORTED_FILE_EXTENSIONS
