from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from typing import TYPE_CHECKING
from datetime import datetime
from app.core.database import Base
from .product_order_assoc import association_table

if TYPE_CHECKING:
    from .product import Product


class Order(Base):
    promo: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        server_default=func.now()
    )

    products: Mapped[list['Product']] = relationship(
        secondary=association_table,
        back_populates='orders'
    )
