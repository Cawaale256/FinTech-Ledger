from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.accounts import Account
from app.schemas.accounts import AccountCreate, AccountResponse

from app.core.security import get_current_user


from app.models.users import User

router = APIRouter(tags=["Accounts"])


@router.post("/", response_model=AccountResponse , status_code=status.HTTP_201_CREATED)
async def create_account(
    payload:AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # The user_id comes from the JWT
    # Meaning the user cannot impersonate another user.
    # Ownership is guaranteed automatically
    # Derive user_id from authenticated token
    user_id = current_user.id
   
    #  Prevent duplicate wallet in same currency
    existing = (
    db.query(Account)
    .filter(Account.user_id == user_id, Account.currency == payload.currency)
    .first()
    )   

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= "User has already Wallet in this currency"
        )
    # Create wallet with safe defaults
    account = Account(
        user_id = current_user.id,
        currency = payload.currency,
        balance = 100
    )
    db.add(account)
    db.commit()
    db.refresh(account)

    return account

