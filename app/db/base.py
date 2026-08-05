# Shared SQLAlchemy Base class for the entire application.
# ---------------------------------------------------------
# This file defines a single declarative Base instance that all ORM models
# must inherit from. Having one global Base ensures:
#
# - Alembic can correctly detect all models via Base.metadata
# - Autogenerate migrations work reliably across the whole project
# - Models remain consistent and discoverable by the ORM
# - Clean project structure: models live in app/models/, Base lives in app/db/
#
# Every model should import Base from this file:
#     from app.db.base import Base
#
# This avoids multiple Base instances, prevents migration issues,
# and follows best practices for FastAPI + SQLAlchemy applications.


from sqlalchemy.orm import declarative_base

Base = declarative_base()

