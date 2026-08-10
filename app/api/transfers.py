from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.users import User
from app.models.accounts import Account
from app.models.transfers import Transfer
from app.models.idempotency import IdempotencyRecord
from app.schemas.transfers import TransferCreate, TransferResponse
from app.schemas.errors import ErrorResponse   

import hashlib

router = APIRouter(tags=["Transfers"])


@router.post("/", response_model=TransferResponse)
async def create_transfer(
    payload: TransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    idempotency_key: str = Header(None, alias="Idempotency-key")
):
    # Idempotency-Key header
    if not idempotency_key:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                detail="Idempotency-Key header is required",
                code="IDEMPOTENCY_KEY_MISSING",
                hint="Include 'Idempotency-Key' header for safe retries"
            ).model_dump()
        )

    # Compute request hash (payload fingerprint)
    request_hash = hashlib.sha256(payload.model_dump_json().encode()).hexdigest()

    # Check if idempotency record exists
    existing_record = (
        db.query(IdempotencyRecord)
        .filter(
            IdempotencyRecord.idempotency_key == idempotency_key,
            IdempotencyRecord.user_id == current_user.id
        )
        .first()
    )

    # If record exists → replay response
    if existing_record:
        if existing_record.request_hash != request_hash:
            raise HTTPException(
                status_code=409,
                detail=ErrorResponse(
                    detail="Idempotency conflict: request payload differs from original",
                    code="IDEMPOTENCY_CONFLICT",
                    hint="Use a new idempotency key for different payloads"
                ).model_dump()
            )
        return existing_record.response_body

    # Fetch accounts
    source = db.query(Account).filter(Account.id == payload.source_account_id).first()
    destination = db.query(Account).filter(Account.id == payload.destination_account_id).first()

    if not source or not destination:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                detail="Account not found",
                code="ACCOUNT_NOT_FOUND",
                hint="Verify source_account_id and destination_account_id"
            ).model_dump()
        )

    # Ownership enforcement
    if source.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail=ErrorResponse(
                detail="Forbidden: cannot transfer from another user's account",
                code="FORBIDDEN_TRANSFER",
                hint="Transfers must originate from accounts owned by the authenticated user"
            ).model_dump()
        )

    # Currency match
    if source.currency != destination.currency:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorResponse(
                detail="Currencies do not match",
                code="CURRENCY_MISMATCH",
                hint="Source and destination accounts must share the same currency"
            ).model_dump()
        )

    # Balance check
    if source.balance < payload.amount:
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                detail="Insufficient funds",
                code="INSUFFICIENT_FUNDS",
                hint="Ensure the source account has enough balance"
            ).model_dump()
        )

    # Atomic transfer
    try:
        source.balance -= payload.amount
        destination.balance += payload.amount

        transfer = Transfer(
            source_account_id=payload.source_account_id,
            destination_account_id=payload.destination_account_id,
            amount=payload.amount,
            status="success",
            user_id=current_user.id
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
