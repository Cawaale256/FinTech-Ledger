import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from app.db.base import Base



class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # The idempotency key sent by the client
    idempotency_key = Column(String, nullable=False, unique=True)

    # User-scoped multitenancy: each user is their own tenant
    user_id = Column(UUID(as_uuid=True), nullable=False)

    # Prevents reusing the same key with different payloads
    request_hash = Column(String, nullable=False)

    # Cached response
    response_body = Column(JSONB, nullable=False)

    # Replay must return the same status code
    status_code = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
