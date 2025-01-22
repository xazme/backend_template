from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from app.core.schemas import UserCreate, UserResponce, UserUpdate
from app.core.models import User


async def create_user(session: AsyncSession, user_info: UserCreate) -> UserResponce:
    new_user = User(user_info.name, user_info.email)
    new_user = User(**user_info.model_dump())

    async with session.begin():
        session.add(new_user)

    return UserResponce.from_orm(new_user)


async def get_users(session: AsyncSession) -> list[UserResponce]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(statement=stmt)
    users = result.scalars().all()

    return [UserResponce.from_orm(user) for user in users]


async def get_user_by_name(session: AsyncSession, searched_name: str) -> UserResponce | None:
    stmt = select(User).where(User.name == searched_name).limit(1)
    result: Result = await session.execute(statement=stmt)
    user = result.scalars().first()

    if user is None:
        return None

    return UserResponce.from_orm(user)


async def delete_user_by_name(session: AsyncSession, searched_name: str) -> UserResponce | None:
    stmt = select(User).where(User.name == searched_name)
    result: Result = await session.execute(statement=stmt)
    user_to_delete = result.scalars().first()

    if user_to_delete is None:
        return None

    async with session.begin():
        session.delete(user_to_delete)

    return UserResponce.from_orm(user_to_delete)


async def update_user_by_name(session: AsyncSession, searched_name: str, new_info: UserUpdate) -> UserResponce | None:
    stmt = select(User).where(User.name == searched_name)
    result: Result = await session.execute(statement=stmt)
    user_to_update = result.scalars().first()

    if user_to_update is None:
        return None

    user_to_update.name = new_info.name
    user_to_update.email = new_info.email

    async with session.begin():
        session.add(user_to_update)

    return UserResponce.from_orm(user_to_update)
