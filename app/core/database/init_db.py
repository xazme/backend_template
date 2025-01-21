from app.core.database.engine import engine
from app.core.database.base import Base


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        yield
        await conn.run_sync(Base.metadata.create_all)
