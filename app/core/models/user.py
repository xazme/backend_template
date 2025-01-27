from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.core.database import Base

if TYPE_CHECKING:
    from .task import Task


class User(Base):

    name: Mapped[str] = mapped_column(String(50), index=True)
    email: Mapped[str] = mapped_column(String(), unique=True, index=True)

    task: Mapped[list['Task']] = relationship(back_populates='task')
