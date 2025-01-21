from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class UserCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: Annotated[EmailStr, Field(...)]


class UserUpdate(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: Annotated[EmailStr, Field(...)]


class UserResponce(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        orm_mode = True
