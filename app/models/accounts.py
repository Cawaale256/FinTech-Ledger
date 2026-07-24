import uuid
from sqlalchemy import Column, String, Numeric, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), nullable=False)

    currency = Column(String, nullable=False, default="USD")

    balance = Column(Numeric(18, 2), nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "currency", name="uq_user_currency"),
    )

    # Transfer relationships (correct)
    sent_transfers = relationship(
        "Transfer",
        foreign_keys="Transfer.source_account_id",
        back_populates="source_account"
    )

    received_transfers = relationship(
        "Transfer",
        foreign_keys="Transfer.destination_account_id",
        back_populates="destination_account"
    )
