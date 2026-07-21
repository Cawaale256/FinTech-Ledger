from fastapi import APIRouter

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)

@router.get("/")
def list_transactions():
    return {"message": "transactions list"}
