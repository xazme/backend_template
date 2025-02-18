from fastapi import Form, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidSignatureError
from app.auth import TokensGenerator, HashOperations, ExcHelper, JWTOperations
from schm_test import UserSchema

oauth2_access_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login")

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


class AuthrizationService:

    @staticmethod
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


class UserService:
    @staticmethod
    def get_user_payload(token=Depends(oauth2_access_scheme)):
        try:
            payload = JWTOperations.decode_jwt(token=token)
        except InvalidSignatureError:
            raise ExcHelper.raise_http_403_forbiden(detail="invalid token")
        return payload

    @staticmethod
    def get_user_from_database(payload: dict):
        username = payload.get("sub")
        if not (user := users_db.get(username)):
            raise ExcHelper.raise_http_401_not_auth("invalid user")
        else:
            return user


class TokenService:
    @staticmethod
    def validate_token(payload: dict, selected_token: str):
        if selected_token not in [
            TokensGenerator.ACCESS_TOKEN,
            TokensGenerator.REFRESH_TOKEN,
        ]:
            raise ExcHelper.raise_http_403_forbiden("not valid token format")

        token_type = payload.get(TokensGenerator.TOKEN_TYPE_FIELD)

        print(f"дан {token_type}, искомый {selected_token}")
        print(payload)
        if token_type != selected_token:
            raise ExcHelper.raise_http_403_forbiden("invalid token")
        return True


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
        self,
        payload: dict = Depends(UserService.get_user_payload),
    ):
        TokenService.validate_token(payload, self.token_type)
        return UserService.get_user_from_database(payload)


# ЕБАТЬ МЕНЯ КОПАТЬ, ЧЕ Я ТУТ НАМУТИЛ
user_by_refresh = UserGetterFromToken(TokensGenerator.REFRESH_TOKEN)
user_by_access = UserGetterFromToken(TokensGenerator.ACCESS_TOKEN)
