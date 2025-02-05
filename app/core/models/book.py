from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from .author import Author
    from .borrowinglist import BookReaderAssoc


class Book(Base):
    title: Mapped[str] = mapped_column(String(100))
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    availible: Mapped[bool] = mapped_column(default=True, server_default="True")
    author: Mapped["Author"] = relationship(back_populates="books")

    reader_info: Mapped[list["BookReaderAssoc"]] = relationship(
        back_populates="book",
    )
