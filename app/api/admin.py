from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.models.users import User
from app.models.accounts import Account
from app.models.transfers import Transfer
from app.schemas.errors import ErrorResponse   # shared ErrorResponse model

router = APIRouter(prefix="", tags=["admin"])


# Admin-only guard
def require_admin(current_user: User):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorResponse(
                detail="Admins only",
                code="ADMIN_REQUIRED",
                hint="Only users with role='admin' may access this endpoint"
            ).model_dump()
        )
    return current_user


# Get all users
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    return db.query(User).all()


# Get all accounts
@router.get("/accounts")
def get_all_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    return db.query(Account).all()


# Get all transfers
@router.get("/transfers")
def get_all_transfers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    return db.query(Transfer).all()


# Delete a user (admin only)
@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorResponse(
                detail="User not found",
                code="USER_NOT_FOUND",
                hint="Verify the user_id is correct"
            ).model_dump()
        )

    db.delete(user)
    db.commit()
    return None
