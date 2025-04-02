from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

class PetBase(BaseModel):
    name: str
    breed: str
    age: int

class PetCreate(PetBase):
    pass

class PetResponse(PetBase):
    id: int
    adopted: bool

    class Config:
        from_attributes = True

class PetUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    breed: Optional[str] = None
    description: Optional[str] = None

class AdoptionResponse(BaseModel):
    id: int
    pet_id: int
    user_id: int
    adoption_date: datetime

    class Config:
        from_attributes = True  # For compatibility with SQLAlchemy ORM