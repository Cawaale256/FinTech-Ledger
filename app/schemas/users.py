from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime


# Shared fields (internal use)
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    role: str = Field(..., description="User role: user or admin")


# Input schema: Client → API (Registration)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Plain password for registration")


# Input schema: Client → API (Login)
class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")


# Output schema: API → Client (Safe response)
class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True
    }



