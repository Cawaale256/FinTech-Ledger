import uuid
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    source_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id"),
        nullable=False,
    )

    destination_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id"),
        nullable=False,
    )

    amount = Column(Numeric(18, 2), nullable=False)

    idempotency_key = Column(String, nullable=False)

    status = Column(String, nullable=False)  # "success" or "failed"

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Prevent duplicate transfers for same wallet + idempotency key
    __table_args__ = (
        UniqueConstraint("source_account_id", "idempotency_key", name="uq_idempotency"),
    )

    # Relationship back to Account
    source_account = relationship(
        "Account",
        back_populates="sent_transfers",
        foreign_keys=[source_account_id]
    )

    destination_account = relationship(
        "Account",
        back_populates="received_transfers",
        foreign_keys=[destination_account_id]
    )
