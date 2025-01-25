from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Dildo(Base):

    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
