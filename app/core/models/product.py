from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING
from .product_order_assoc import association_table

if TYPE_CHECKING:

    from .order import Order


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    orders: Mapped[list['Order']] = relationship(
        secondary=association_table,
        back_populates='products'
    )
