from fastapi import APIRouter

router = APIRouter(tags=["Accounts"])

@router.get("/")
def list_accounts():
    return {"message": "accounts list"}
