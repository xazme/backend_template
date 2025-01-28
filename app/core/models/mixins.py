from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class UserRelationShipMixins:

    _user_id_unique: bool = False
    _user_back_populates: str | None = None
    _user_is_nullabe: bool = False

    @declared_attr
    def user_id(cls):
        return mapped_column(ForeignKey('user.id'), unique=cls._user_id_unique, nullable=cls._user_is_nullabe)

    @declared_attr
    def user(cls):
        return relationship('User', back_populates=cls._user_back_populates)
