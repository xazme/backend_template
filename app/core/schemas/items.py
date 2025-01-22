from pydantic import BaseModel, Field
from typing import Annotated


class ItemCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    weight: Annotated[float, Field(..., gt=0, lt=100)]


class ItemUpdate(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    weight: Annotated[float, Field(..., gt=0, lt=100)]


class ItemsResponce(BaseModel):
    id: str
    name: str
    weight: float

    class Config:
        orm_mode = True
