from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt.exceptions import ExpiredSignatureError
from schm_test import UserSchema, TokenInfo
from app.auth import ExcHelper, JWTHelper, HashHelper, JWTMaker

http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/jwt", tags=["JWT TRAINING"], dependencies=[Depends(http_bearer)]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login")

john = UserSchema(
    username="john",
    password=HashHelper.hash_password("sexbomba123"),
    email="jognthenotoleg@gmail.com",
)

oleg = UserSchema(
    username="oleg",
    password=HashHelper.hash_password("iamcoolperson"),
    email="thecoololeg@gmail.com",
)

users_db: dict[str, dict] = {
    john.username: john,
    oleg.username: oleg,
}


def get_user_payload(token=Depends(oauth2_scheme)):
    try:
        payload = JWTHelper.decode_jwt(token=token)
    except ExpiredSignatureError:
        ExcHelper.raise_http_401_not_auth("ошибка на стороне сервера")
    return payload


def get_user_data(payload: dict = Depends(get_user_payload)):

    token_type = payload.get(JWTMaker.TOKEN_TYPE_FIELD)

    if token_type != JWTMaker.ACCESS_TOKEN:
        raise ExcHelper.raise_http_401_not_auth("token error")

    username = payload.get("username")

    if not (user := users_db.get(username)):
        ExcHelper.raise_http_401_not_auth("не удалось найти пользователя")

    return user


def chech_user_status(user: UserSchema = Depends(get_user_data)):
    if not user.active:
        ExcHelper.raise_http_403_forbiden()
    else:
        return user


def validate_loginned_user(
    username=Form(),
    password=Form(),
):
    if not (user := users_db.get(username)):
        ExcHelper.raise_http_401_not_auth(detail="invalid login or password")

    if not HashHelper.check_password(password=password, hashed_password=user.password):
        ExcHelper.raise_http_401_not_auth(detail="invalid login or password")

    return user


def create_jwt(payload: dict):
    token = JWTHelper.encode_jwt(payload=payload)


@router.post("/login")
async def user_login(user: UserSchema = Depends(validate_loginned_user)):
    access_token = JWTMaker.generate_access_token(user=user)
    refresh_token = JWTMaker.generate_refresh_token(user=user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me")
async def show_user_profile(user: UserSchema = Depends(chech_user_status)):
    return {
        "username": user.username,
    }
