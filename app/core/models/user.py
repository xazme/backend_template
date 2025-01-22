from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base


class User(Base):

    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email
