from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import (
    authenticate_user,
    create_access_token,
    hash_password
)
from app.models.users import User

router = APIRouter(prefix="", tags=["auth"])


@router.post("/register")
def register(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    # Check if user already exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        email=email,
        hashed_password=hash_password(password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # OAuth2 sends email inside "username"
    email = form_data.username 
    # # Authenticate user
    user = authenticate_user(db, email, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Issue JWT token
    token = create_access_token(user)

    return {"access_token": token, "token_type": "bearer"}


