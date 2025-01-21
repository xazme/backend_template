from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.core.database import engine

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


async def get_db():
    async with async_session() as session:
        yield session
