from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
import enum

if TYPE_CHECKING:
    from .task import Task
    from .worker import Worker


class Status(enum.Enum):
    complete = "Complete"
    not_complete = "Not complete"


class TaskWorkerAssoc(Base):

    __table_args__ = (UniqueConstraint("task_id", "worker_id"),)

    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    worker_id: Mapped[int] = mapped_column(ForeignKey("worker.id"))
    status: Mapped[str] = mapped_column(
        Enum(Status),
        default=Status.not_complete.name,
        server_default=Status.not_complete.name,
    )

    task: Mapped["Task"] = relationship(back_populates="worker_info")
    worker: Mapped["Worker"] = relationship(back_populates="task_info")
