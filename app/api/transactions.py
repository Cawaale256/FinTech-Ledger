from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth import get_current_user
from app.models.users import User
from app.models.accounts import Account
from app.models.transfers import Transfer
from app.schemas.transactions import TransactionListResponse

router = APIRouter(tags=["Transactions"])


@router.get("/accounts/{account_id}/transactions", response_model=TransactionListResponse)
async def list_transactions_for_account(
    account_id: str,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    View transfer history for a wallet the user owns.
    Supports pagination (limit + offset).
    """

    # Ownership check

    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    if account.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: cannot view transactions for another user's wallet"
        )

    # Fetch transfers (source OR destination)
    transfers_query = (
        db.query(Transfer)
        .filter(
            (Transfer.source_account_id == account_id) |
            (Transfer.destination_account_id == account_id)
        )
        .order_by(Transfer.created_at.desc())  # newest first
    )

    total = transfers_query.count()

    transfers = transfers_query.limit(limit).offset(offset).all()

    
    # 3. Build response
    return TransactionListResponse(
        account_id=account_id,
        total=total,
        limit=limit,
        offset=offset,
        items=transfers
    )
