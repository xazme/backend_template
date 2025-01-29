from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship

if TYPE_CHECKING:
    from .user import User


class UserRelationMixin:
    _user_back_populates: str | None = None
    _user_id_foreign_key: str | None = None

    @declared_attr
    def user(cls):
        return relationship('User', back_populates=cls._user_back_populates)

    @declared_attr
    def user_id(cls):
        return mapped_column(Integer, ForeignKey(cls._user_id_foreign_key))
