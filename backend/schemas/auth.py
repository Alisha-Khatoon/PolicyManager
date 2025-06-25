from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    enterprise_id: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: str
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class EnterpriseCreate(BaseModel):
    name: str
    industry: str
    admin_email: EmailStr
    admin_password: str
    domain: str