"""File utilities."""

from pathlib import Path


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_filename(filename: str) -> str:
    sanitized = "".join(char if char.isalnum() or char in {".", "_", "-"} else "_" for char in filename)
    return sanitized or "document"


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()
