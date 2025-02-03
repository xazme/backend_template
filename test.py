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
    expire_on_commit=False,
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_order(session: AsyncSession, promo: str | None):
    new_order = Order(promo=promo)
    session.add(new_order)
    await session.commit()


async def create_products(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
):
    new_product = Product(name=name, description=description, price=price)
    session.add(new_product)
    await session.commit()


async def main():
    await create_tables()
    async with async_session() as session:
        order1 = await create_order(
            session=session,
            promo="jopa",
        )

        order1 = await create_order(
            session=session,
            promo="bebra",
        )

        mouse = await create_products(
            session=session,
            name="mouser",
            description="super puper mouse",
            price=1300,
        )


asyncio.run(main())
