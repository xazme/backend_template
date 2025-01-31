import asyncio
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Base, engine
from app.core.models import User, Profile, Task, Product, Order

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.core.database import engine

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_order(ses: AsyncSession, promo: str | None):
    order = Order(promocode=promo)
    ses.add(order)
    await ses.commit()
    return order


async def create_product(ses: AsyncSession, name: str, description: str, price: int):
    product = Product(name=name, description=description, price=price)

    ses.add(product)
    await ses.commit()
    return product


async def main():
    await create_tables()
    async with async_session() as ses:
        item1 = await create_product(ses=ses, name='sextoy',
                                     description='c++ book', price=300)
        item2 = await create_product(ses=ses, name='book',
                                     description='david gogings', price=300)

        order1 = await create_order(ses=ses, promo='123YOO')
        order2 = await create_order(ses=ses, promo=None)
        order1 = await ses.scalar(select(Order).where(Order.id == order1.id).options(selectinload(Order.products)))
        order2 = await ses.scalar(select(Order).where(Order.id == order2.id).options(selectinload(Order.products)))
        order1.products.append(item1)
        order2.products.append(item1)

        await ses.commit()
asyncio.run(main())
