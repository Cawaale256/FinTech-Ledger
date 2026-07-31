from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List


class TransactionItem(BaseModel):
    id: UUID
    source_account_id: UUID
    destination_account_id: UUID
    amount: float
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class TransactionListResponse(BaseModel):
    account_id: UUID
    total: int
    limit: int
    offset: int
    items: List[TransactionItem]
