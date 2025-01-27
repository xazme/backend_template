from typing import TYPE_CHECKING
from app.core.database import Base
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User


class Task(Base):
    title: Mapped[str] = mapped_column(String(100), index=True)
    body: Mapped[str] = mapped_column(Text, default="", server_default="")

    id: Mapped[int] = mapped_column(ForeignKey(
        'user.id'), primary_key=True, index=True)

    user: Mapped['User'] = relationship(back_populates="")
