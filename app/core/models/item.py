from sqlalchemy.orm import Mapped, mapped_column
from core.database.base import Base


class Items(Base):
    __tablename__ = 'items'

    name: Mapped[str] = mapped_column(index=True)
    weight: Mapped[float] = mapped_column(index=True)

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
