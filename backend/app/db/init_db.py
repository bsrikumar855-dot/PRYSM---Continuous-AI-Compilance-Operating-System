"""Database initialization."""

from app.core.config import settings
from app.db.base import Base, import_models
from app.db.session import engine


def init_db() -> None:
    """Create all directories and database tables."""
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.report_dir.mkdir(parents=True, exist_ok=True)
    settings.chroma_persist_dir.mkdir(parents=True, exist_ok=True)
    import_models()
    Base.metadata.create_all(bind=engine)
