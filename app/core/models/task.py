from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text

from app.core.database import Base
from .mixins import UserRelationMixin


class Task(UserRelationMixin, Base):

    _user_back_populates = 'tasks'
    _user_id_foreign_key = 'user.id'

    title: Mapped[str] = mapped_column(
        String(50),
        index=True
    )

    description: Mapped[str] = mapped_column(
        Text,
        default='',
        server_default='',
    )
