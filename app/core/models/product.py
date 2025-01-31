from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import TYPE_CHECKING
from app.core.database import Base

if TYPE_CHECKING:
    from .order import Order


class Product(Base):
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(300))
    price: Mapped[int] = mapped_column(Integer())

    orders: Mapped[list['Order']] = relationship(
        secondary='order_product_association', back_populates='products')
