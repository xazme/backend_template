from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from .taskworkerassoc import TaskWorkerAssoc


class Worker(Base):
    name: Mapped[str] = mapped_column(String(30), index=True)
    email: Mapped[str] = mapped_column(String(50), index=True)

    task_info: Mapped[list["TaskWorkerAssoc"]] = relationship(back_populates="worker")
