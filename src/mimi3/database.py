"""SQLAlchemy DB connection setup."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Check if we're in testing mode
is_testing = os.environ.get("TESTING", "False").lower() in ("true", "1", "t")

# Configure database connection based on environment
if is_testing:
    # Use SQLite for testing
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Use the configured PostgreSQL database
    from .settings import settings
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create tables (idempotent)."""
    from .models import Base
    Base.metadata.create_all(bind=engine)
