from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime


class User(Document):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    roles: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

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


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    roles: Optional[List[str]] = None


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
