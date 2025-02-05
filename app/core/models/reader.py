from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from .borrowinglist import BookReaderAssoc


class Reader(Base):
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))

    book_info: Mapped[list["BookReaderAssoc"]] = relationship(back_populates="reader")
