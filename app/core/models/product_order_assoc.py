from sqlalchemy import Table, ForeignKey, Column, Integer, UniqueConstraint
from app.core.database import Base

association_table = Table(
    "association_table",
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column("order_id", ForeignKey("order.id"), nullable=False),
    Column("product_id", ForeignKey("product.id"), nullable=False),
    UniqueConstraint('order_id', 'product_id', name="indx_uniq_prod_order"),
)
