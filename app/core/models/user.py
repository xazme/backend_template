from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.core.database import Base

if TYPE_CHECKING:
    from .task import Task
    from .profile import Profile


class User(Base):

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
    )

    email: Mapped[str] = mapped_column(
        String(),
        unique=True,
    )

    tasks: Mapped[list['Task']] = relationship(back_populates='user')
    profile: Mapped['Profile'] = relationship(back_populates='user')

    def __str__(self):
        return f"username = {self.username},email = {self.email}"
