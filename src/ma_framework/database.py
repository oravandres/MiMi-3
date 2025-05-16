"""SQLAlchemy engine & session factory."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings

engine = create_engine(settings.database_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db() -> None:
    """Create tables (idempotent)."""
    from .models import Base  # noqa: F401
    Base.metadata.create_all(bind=engine)
