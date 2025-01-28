# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from sqlalchemy.engine import Result
# from app.core.schemas import ProfileCreate, ProfileUpdate, ProfileResponce
# from app.core.models import Profile


# async def create_profile(session: AsyncSession, profile_settings: ProfileCreate):
#     profile = Profile(**profile_settings.model_dump())

#     session.add(profile)
#     await session.commit()

#     return ProfileResponce.model_validate(profile)


# async def find_profile_by_user_name(session: AsyncSession, searched_username: str):
#     stmt = select(Profile).where(Profile.name == searched_username)
#     result: Result = await session.execute(stmt)
#     user = result.scalars().first()

#     if result is None:
#         return None

#     return ProfileResponce.model_validate(user)

# # async def update(session)
