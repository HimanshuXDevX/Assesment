from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from utils.auth import hash_password


class User(Document):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    roles: List[str] = Field(default_factory=list)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    async def set_password(self, raw_password: str):
        """Hashes and sets user's password."""
        self.password = hash_password(raw_password)

    async def save(self):
        self.updated_at = datetime.utcnow()
        return await super().save()

    class Settings:
        name = "User"

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    roles: List[str] = []
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    roles: Optional[List[str]] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: PydanticObjectId
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str]
    roles: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
