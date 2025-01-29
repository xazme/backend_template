from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text

from app.core.database import Base
from .mixins import UserRelationMixin


class Profile(UserRelationMixin, Base):

    _user_back_populates = 'profile'
    _user_id_foreign_key = 'user.id'

    first_name: Mapped[str | None] = mapped_column(
        String(30),
        index=True,
    )

    second_name: Mapped[str | None] = mapped_column(
        String(30),
        default='',
        server_default='',
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
    )
