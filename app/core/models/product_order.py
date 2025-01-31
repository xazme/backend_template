from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class OrderProductAssociation(Base):
    __tablename__ = 'order_product_association'
    __table_args__ = (
        UniqueConstraint('product_id', 'order_id',
                         name='idx_unique_order_product')
    )
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
