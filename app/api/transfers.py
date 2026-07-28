from fastapi import APIRouter, Depends,status,HTTPException
from app.models.transfers import Transfer
from app.models.accounts import Account
from app.schemas.transfers import TransferCreate, TransferResponse
from sqlalchemy.orm import Session
from app.db.session import get_db


router = APIRouter( tags=["Transfers"])

@router.get("/")
def list_transfers():
    return {"message": "transfers list"}
