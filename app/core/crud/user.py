from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models.models import User


async def create_user(name: str, email: str, session: AsyncSession) -> User:
    new_user = User(name=name, email=email)
    session.add(new_user)
    await session.commit()
    return new_user
