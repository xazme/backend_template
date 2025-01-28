from typing import TYPE_CHECKING
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .mixins import UserRelationShipMixins


class Profile(Base, UserRelationShipMixins):

    _user_back_populates = 'profile'

    first_name: Mapped[str | None] = mapped_column(String(30))
    second_name: Mapped[str | None] = mapped_column(String(30))
    bio: Mapped[str | None] = mapped_column(String(300))
