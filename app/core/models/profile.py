from typing import TYPE_CHECKING
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

if TYPE_CHECKING:
    from .mixins import UserRelationShipMixins


class Profile(UserRelationShipMixins, Base):
    _user_back_populates = 'profile'
    _user_id_unique = True

    first_name: Mapped[str | None] = mapped_column(String(30))
    second_name: Mapped[str | None] = mapped_column(String(30))
    bio: Mapped[str | None] = mapped_column(String(300))
