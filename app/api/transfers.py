from fastapi import APIRouter

router = APIRouter( tags=["Transfers"])

@router.get("/")
def list_transfers():
    return {"message": "transfers list"}
