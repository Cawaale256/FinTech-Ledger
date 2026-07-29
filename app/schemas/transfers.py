from pydantic import BaseModel, Field, field_validator ,model_validator
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class TransferCreate(BaseModel):
    source_account_id : UUID = Field(..., description="Wallet sending the funds")
    destination_account_id: UUID = Field(..., description="Wallet receiving the funds")
    amount: Decimal = Field(...,description="Amount to transfer, must be > 0")

    # Ensure transfer amount is positive
    @field_validator("amount")
    def validate_amount(cls, v):
        if v <= 0:
              raise ValueError("Amount must be greater than Zero")
        return v

    # Prevent transfers between the same account
    @model_validator(mode="after")
    def validate_accounts(self):
        if self.source_account_id == self.destination_account_id:
            raise ValueError("source_account_id and destination_account_id must differ")
        return self
    # # Prevent transfers between the same account
    # @field_validator("destination_account_id")
    # def validate_accounts(cls, dest, value):
    #     src = values.get("source_account_id")
    #     if src and dest == src:
    #         raise ValueError("source_account_id and destination_account_id must differ")
    #     return dest

    
class TransferResponse(BaseModel):
    id : UUID
    source_account_id : UUID
    destination_account_id : UUID
    amount : Decimal
    status : str
    created_at:datetime

    model_config = {
           "from_attributes": True
       }