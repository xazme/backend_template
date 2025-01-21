from sqlalchemy.ext.asyncio import AsyncSession
from app.core.schemas.user import UserCreate, UserResponce, UserUpdate
from app.core.models.user import User


async def create_user(user_create: UserCreate, session: AsyncSession) -> User:
    user = User(name=user_create.name, email=user_create.email)
    session.add(user)
    await session.commit()
    return user_create
