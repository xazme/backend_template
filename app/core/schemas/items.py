from pydantic import BaseModel, Field
from typing import Annotated


class ItemCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    weight: Annotated[float, Field(..., gt=0, lt=100)]


class ItemCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    weight: Annotated[float, Field(..., gt=0, lt=100)]


class UserResponce(BaseModel):
    id: str
    name: str
    email: float

    class Config:
        orm_mode = True
