from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.accounts import Account
from app.models.transfers import Transfer
from app.schemas.accounts import AccountCreate, AccountResponse
from app.auth import get_current_user


router = APIRouter(tags=["Accounts"])


@router.post("/", response_model=AccountResponse , status_code=status.HTTP_201_CREATED)
async def create_account(
    payload:AccountCreate,
    db: Session = Depends(get_db),
    current_user: user = Depends(get_current_user)
):
    
    # Ownership check : user can only create their own wallet
    if payload.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: cannnot create wallet for another user"
        )
    # In real auth: current_user.id must match payload.user_id
    # For now, assume user_id is trusted or mock auth
    # Example:
    # if payload.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Forbidden: cannot create wallet for another user")
    
    #  Prevent duplicate wallet in same currency
    existing = (
    db.query(Account)
    .filter(Account.user_id == payload.user_id, Account.currency == payload.currency)
    .first()
    )   

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= "User has already Wallet in this currency"
        )
    # Create wallet with safe defaults
    account = Account(
        user_id = payload.user_id,
        currency = payload.currency,
        balance = 100
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

