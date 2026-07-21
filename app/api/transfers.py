from fastapi import APIRouter

router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"],
)

@router.get("/")
def list_transfers():
    return {"message": "transfers list"}
