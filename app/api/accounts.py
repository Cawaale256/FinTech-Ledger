from fastapi import APIRouter

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)

@router.get("/")
def list_accounts():
    return {"message": "accounts list"}
