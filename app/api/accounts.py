from fastapi import APIRouter, Depends,status,HTTPException
from app.models.accounts import Account
from app.schemas.accounts import AccountCreate, AccountResponse
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter(tags=["Accounts"])

@router.get("/", response_model=AccountResponse)
def list_accounts(Account: AccountResponse, db: Session = Depends(get_db)):
    return db.query(Account).all()


@router.post("/", response=AccountResponse , status_code=status.HTTP_201_CREATED)
async def create_account(payload:AccountCreate, db: Session = Depends(get_db)):
     # Ownership check (Day 7 requirement)
    # In real auth: current_user.id must match payload.user_id
    # For now, assume user_id is trusted or mock auth
    # Example:
    # if payload.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Forbidden: cannot create wallet for another user")
    
    # Duplicate wallet check (Day 1 requirement)
    existing = (
    db.query(Account)
    .filter(Account.user_id == payload.user_id, Account.currency == payload.currency)
    .first()
    )   

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            details= "User has already Wallet in this currency"
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