from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from .book import Book
    from .reader import Reader


class BookReaderAssoc(Base):
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    reader_id: Mapped[int] = mapped_column(ForeignKey("reader.id"))
    borrow_date: Mapped[datetime] = mapped_column(
        default=datetime.now, server_default=func.now()
    )

    # Assoc -> book
    book: Mapped["Book"] = relationship(back_populates="reader_info")

    # Assoc -> reader
    reader: Mapped["Reader"] = relationship(back_populates="book_info")
