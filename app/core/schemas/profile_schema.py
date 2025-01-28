from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated


class ProfileCreate(BaseModel):
    first_name: Annotated[str, Field(None, max_length=30)]
    second_name: Annotated[str, Field(None, max_length=30)]
    bio: Annotated[str, Field(None, max_length=300)]


class ProfileUpdate(ProfileCreate):
    pass


class ProfileResponce(BaseModel):
    first_name: str
    second_name: str
    bio: str

    model_config = ConfigDict(from_attributes=True)
