from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from schm_test import UserSchema, TokenInfo
from app.auth import ExcHelper, HashOperations, TokensGenerator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/me")

router = APIRouter(prefix="/jwt", tags=["JWT TRAINING"])

john = UserSchema(
    username="john",
    password=HashOperations.hash_password("sexbomba123"),
    email="jognthenotoleg@gmail.com",
)

oleg = UserSchema(
    username="oleg",
    password=HashOperations.hash_password("iamcoolperson"),
    email="thecoololeg@gmail.com",
)

users_db: dict[str, dict] = {
    john.username: john,
    oleg.username: oleg,
}


def auth_user(
    username: str = Form(),
    password: str = Form(),
):
    if not (user := users_db.get(username)):
        ExcHelper.raise_http_401_not_auth("invalid username")

    if not HashOperations.validate_password(
        password=password, hashed_password=user.password
    ):
        ExcHelper.raise_http_401_not_auth("invalid password")

    return user


def get_user_token(token=Depends(oauth2_scheme)):
    pass


def get_user_data(payload: dict = Depends(get_user_token)):
    pass


def check_user_status(user: UserSchema = Depends(get_user_data)):
    if not user.active:
        return ExcHelper.raise_http_403_forbiden("user is not active")
    else:
        return user


@router.post("/login")
async def auth_user(user: UserSchema = Depends(auth_user)):
    access_token = TokensGenerator.generate_access_token(user=user)
    refresh_token = TokensGenerator.generate_refresh_token(user=user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me")
async def auth_user_profile(user: UserSchema = Depends(...)):
    pass
