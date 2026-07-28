from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal
from datetime import datetime

# Input schema Client -> API :what the client is allowed to send
class AccountCreate(BaseModel):
    user_id: UUID = Field(..., description="ID of the authenticated user creating the wallet")
    currency: str = Field("USD", description="Wallet currency, defaults to USD")

# Output Schema API -> Client:what the API returns
class AccountResponse(BaseModel):
    id: UUID
    user_id: UUID
    currency: str
    balance: Decimal
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
