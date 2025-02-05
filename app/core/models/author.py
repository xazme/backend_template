from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from .book import Book


class Author(Base):
    name: Mapped[str] = mapped_column(String(50))
    books: Mapped[list["Book"]] = relationship(back_populates="author")
