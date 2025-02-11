from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from .taskworkerassoc import TaskWorkerAssoc


class Task(Base):
    title: Mapped[str] = mapped_column(String(30), index=True)
    description: Mapped[str] = mapped_column(String(2000), index=True)

    worker_info: Mapped[list["TaskWorkerAssoc"]] = relationship(back_populates="task")
