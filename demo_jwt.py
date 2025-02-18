from fastapi import APIRouter, Depends
from datetime import datetime
from schm_test import UserSchema, TokenInfo
from app.auth import TokensGenerator
from validators import AuthrizationService, user_by_access, user_by_refresh

router = APIRouter(prefix="/jwt", tags=["JWT TRAINING"])


@router.post("/login")
async def auth_user(user: UserSchema = Depends(AuthrizationService.auth_user)):
    access_token = TokensGenerator.generate_access_token(user=user)
    refresh_token = TokensGenerator.generate_refresh_token(user=user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model_exclude_none=True)
async def refresh_access_token(user: UserSchema = Depends(user_by_refresh)):
    access_token = TokensGenerator.generate_access_token(user=user)
    return TokenInfo(access_token=access_token)


@router.get("/me")
async def auth_user_profile(user: UserSchema = Depends(user_by_access)):
    return {"username": user.username}
