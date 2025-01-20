from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from core.database.engine import engine

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


async def get_db():
    async with async_session() as session:
        yield session
