from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class TaskCreate(BaseModel):
    title: Annotated[str, Field(..., max_length=100)]
    body: Annotated[str, Field(..., max_length=500)]


class TaskUpdate(TaskCreate):
    pass


class TaskResponce(BaseModel):
    title: str
    body: str

    model_config = ConfigDict(from_attributes=True)
