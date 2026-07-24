from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, func

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    currency = Column(String, nullable=False, default="USD")
    balance = Column(Numeric(12, 2), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship mapping 
    user = relationship("User", back_populates="accounts")

    transactions = relationship(
        "Transaction",
        back_populates="account",
        cascade="all, delete-orphan"
    )

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
