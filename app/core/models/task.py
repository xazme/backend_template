from typing import TYPE_CHECKING
from app.core.database import Base
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from .mixins import UserRelationShipMixins


class Task(UserRelationShipMixins, Base):
    _user_back_populates = 'task'
    _user_id_unique = False

    title: Mapped[str] = mapped_column(String(100), index=True)
    body: Mapped[str] = mapped_column(Text, default="", server_default="")
