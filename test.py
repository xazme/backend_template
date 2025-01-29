import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Base, engine
from app.core.models import User

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


async def add_user(username: str, email: str, session: AsyncSession):
    new_user = User(username=username, email=email)
    session.add(new_user)
    await session.commit()
    print(new_user)


async def main():
    await create_tables()
    async with async_session() as ses:
        await add_user('alex', 'alextheuser@gmail.com', session=ses)

asyncio.run(main())
