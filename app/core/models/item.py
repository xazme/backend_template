from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Item(Base):

    name: Mapped[str] = mapped_column(index=True)
    weight: Mapped[float] = mapped_column(index=True)

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
