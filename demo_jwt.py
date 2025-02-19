from fastapi import APIRouter, Depends, Response
from schm_test import UserSchema, TokenInfo
from fastapi.security import HTTPBearer
from app.auth import TokensGenerator
from validators import AuthrizationService, user_by_access, user_by_refresh

# dependencies=[Depends(http_bearer)
http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/jwt", tags=["JWT TRAINING"], dependencies=[Depends(http_bearer)]
)


@router.post("/login")
async def auth_user(
    response: Response,
    user: UserSchema = Depends(AuthrizationService.auth_user),
):
    access_token = TokensGenerator.generate_access_token(user=user)
    refresh_token = TokensGenerator.generate_refresh_token(user=user)

    response.set_cookie(
        key=TokensGenerator.REFRESH_TOKEN,
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model_exclude_none=True)
async def refresh_access_token(
    response: Response,
    user: UserSchema = Depends(user_by_refresh),
):
    refresh_token = TokensGenerator.generate_refresh_token(user)
    response.set_cookie(
        key=TokensGenerator.REFRESH_TOKEN,
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    access_token = TokensGenerator.generate_access_token(user=user)
    # response.headers["Authorization"] = f"Bearer {access_token}"
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me")
async def auth_user_profile(user: UserSchema = Depends(user_by_access)):
    return {"username": user.username}
