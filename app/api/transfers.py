from fastapi import APIRouter, Depends,status,HTTPException, Header
from app.models.transfers import Transfer
from app.models.accounts import Account
from app.schemas.transfers import TransferCreate, TransferResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
import hashlib
from app.models.idempotency import IdempotencyRecord

router = APIRouter( tags=["Transfers"])


@router.post("/", response_model=TransferResponse)
async def create_transfer( payload:TransferCreate, db: Session=Depends(get_db),
     idempotency_key: str = Header(None, alias="Idempotency-key")
     ):
    # Idempotency-Key header
    if not idempotency_key:
     raise HTTPException(status_code=400,
            detail="Idempotency-Key header is required"
            )
    # Compute request hash (payload fingerprint)
    request_hash = hashlib.sha256(payload.model_dump_json().encode()).hexdigest()

    # Check if idempotency record exists
    record = (
        db.query(IdempotencyRecord)
        .filter(
            IdempotencyRecord.idempotency_key == idempotency_key,
            IdempotencyRecord.user_id == current_user.id   # user-scoped multitenancy
        )
        .first()
    )
    try:
        # Fetch a source wallet
        source = db.query(Account).filter(Account.id == payload.source_id).first()
        # Authorization + user-scoped multitenancy
        if not source:
            raise HTTPException(status_code= 404, detail=" Not found")
        # Fetch a destination wallet
        destination = db.query(Account).filter(Account.id == payload.destination_account_id).first()
        if not destination:
            raise HTTPException(status_code= 404, detail=" Not found")
        # Currency check
        if source.currency != destination.currency:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Currencies do not match") 
        # Balance check
        if source.balance <=  payload.amount:
            raise HTTPException(status_code=400, detail="Insufficient fund")
        # # Apply transfer
        source.balance -=payload.amount
        destination.balance +=payload.amount
    

        transfer = Transfer(
     
            source_account_id=payload.source_account_id,
            destination_account_id=payload.destination_account_id,
            amount=payload.amount,
            status="success",
            user_id=current_user_id # user-scpoed tenancy
        
        )

        db.add_all([source, destination, transfer])
        db.commit()
        db.refresh(transfer)

        # Save idempotency record
        response_body = TransferResponse.model_validate(transfer).model_dump()

        record = IdempotencyRecord(
                    idempotency_key=idempotency_key,
                    user_id=current_user.id,
                    request_hash=request_hash,
                    response_body=response_body,
                    status_code="200"
                )

        db.add(record)
        db.commit()
        
        return response_body
    
    except Exception as e:
        db.rollback()
        raise e