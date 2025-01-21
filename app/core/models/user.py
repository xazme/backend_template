from sqlalchemy.orm import Mapped, mapped_column
from core.database.base import Base


class User(Base):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(ndex=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email
