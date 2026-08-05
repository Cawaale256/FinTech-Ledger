from sqlalchemy import create_engine
import os

# 
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,        # avoids stale connections
    echo=False                 # set True for debugging SQL
)
# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    
