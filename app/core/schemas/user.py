from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated


class UserCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: Annotated[EmailStr, Field(...)]


class UserUpdate(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    email: Annotated[EmailStr, Field(...)]


class UserResponce(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)
