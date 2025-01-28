from app.core.crud import create_user, get_user_by_name, get_users, update_user_by_name, delete_user_by_name
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.core.schemas import UserResponce, UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/users')


@router.get('/', response_model=list[UserResponce])
async def get_all_users(session: AsyncSession = Depends(get_db)):
    return await get_users(session=session)


@router.get('/{user_name}', response_model=UserResponce | None)
async def get_user(user_name: str, session: AsyncSession = Depends(get_db)):
    res = await get_user_by_name(session=session, searched_name=user_name)
    if res is None:
        raise HTTPException(status_code=404)
    return res


@router.post('/create_user', response_model=UserCreate)
async def create_new_user(user: UserCreate, session: AsyncSession = Depends(get_db)):
    return await create_user(session=session, user_info=user)


@router.put('/update/{user_name}', response_model=UserResponce | None)
async def update_user(user_name: str, user: UserUpdate, session: AsyncSession = Depends(get_db)):
    res = await update_user_by_name(session=session, new_info=user, searched_name=user_name)
    if res is None:
        raise HTTPException(status_code=404)
    return res


@router.delete('/delete/{user_name}', response_model=UserResponce | None)
async def delete_user(user_name: str, session: AsyncSession = Depends(get_db)):
    res = await delete_user_by_name(session=session, searched_name=user_name)
    if res is None:
        raise HTTPException(status_code=404)
    return res
