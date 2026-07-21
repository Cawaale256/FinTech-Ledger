from fastapi import APIRouter

router = APIRouter(tags=["Transactions"])

@router.get("/")
def list_transactions():
    return {"message": "transactions list"}
