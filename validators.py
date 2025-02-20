from fastapi import Form, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError
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


class TokenService:
    @staticmethod
    def validate_token(payload: dict, selected_token: str):
        if selected_token not in [
            TokensGenerator.ACCESS_TOKEN,
            TokensGenerator.REFRESH_TOKEN,
        ]:
            ExcHelper.raise_http_403_forbiden("not valid token format")

        token_type = payload.get(TokensGenerator.TOKEN_TYPE_FIELD)

        print(f"дан {token_type}, искомый {selected_token}")

        if token_type != selected_token:
            ExcHelper.raise_http_403_forbiden("invalid token")
        return True

    @staticmethod
    def get_refresh_token(request: Request):
        refresh_token = request.cookies.get(TokensGenerator.REFRESH_TOKEN)
        return (
            refresh_token
            if refresh_token
            else ExcHelper.raise_http_401_not_auth("empty token")
        )


class UserService:
    @staticmethod
    def try_decode(token: str):
        try:
            payload = JWTOperations.decode_jwt(token=token)
        except ExpiredSignatureError:
            ExcHelper.raise_http_401_not_auth(detail="Token has expired")
        except Exception as e:

            ExcHelper.raise_http_403_forbiden(detail="Invalid token")
        return payload

    @staticmethod
    def get_user_payload_for_access(
        access_token: str = Depends(oauth2_access_scheme),
    ):
        return UserService.try_decode(access_token)

    @staticmethod
    def get_user_payload_for_refresh(
        refresh_token: str = Depends(TokenService.get_refresh_token),
    ):
        return UserService.try_decode(refresh_token)

    @staticmethod
    def get_user_from_database(payload: dict):
        username = payload.get("sub")
        if not (user := users_db.get(username)):
            ExcHelper.raise_http_401_not_auth("invalid user")
        else:
            return user


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(
        self,
        access_token: dict = Depends(oauth2_access_scheme),
        refresh_payload: dict = Depends(UserService.get_user_payload_for_refresh),
    ):
        if self.token_type == TokensGenerator.ACCESS_TOKEN:
            access_payload = UserService.try_decode(access_token)
            print(access_token)
            TokenService.validate_token(access_payload, self.token_type)
            return UserService.get_user_from_database(access_payload)

        if self.token_type == TokensGenerator.REFRESH_TOKEN:
            TokenService.validate_token(refresh_payload, self.token_type)
            return UserService.get_user_from_database(refresh_payload)


user_by_access = UserGetterFromToken(TokensGenerator.ACCESS_TOKEN)
user_by_refresh = UserGetterFromToken(TokensGenerator.REFRESH_TOKEN)
