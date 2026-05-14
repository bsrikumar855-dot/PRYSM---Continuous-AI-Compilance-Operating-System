"""File utilities."""

import os
from app.config.settings import settings


def ensure_upload_dir():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()
