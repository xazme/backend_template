from sqlalchemy.ext.asyncio import create_async_engine
from app.config.config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)
