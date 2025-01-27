from typing import TYPE_CHECKING
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from .task import Task


class TaskStorage(Base):
    title: Mapped[str] = mapped_column(String(30), unique=True,)
    description: Mapped[str] = mapped_column

    task: Mapped['task'] = relationship(back_populates='tasks')
