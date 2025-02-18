import jwt
import bcrypt
from app.config import settings
from schm_test import UserSchema
from datetime import timedelta, datetime
from fastapi import HTTPException, status


class ExcHelper:
    @staticmethod
    def raise_http_401_not_auth(detail: str = "not auth"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    @staticmethod
    def raise_http_403_forbiden(detail: str = "forbiden"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class JWTOperations:

    @staticmethod
    def encode_jwt(
        payload: dict,
        private_key: str = settings.PRIVATE_KEY,
        algorithm: str = settings.ALGORITHM_TYPE,
        expire_minutes: int = settings.DEFAULT_VALUE_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
    ):
        to_encode = payload.copy()
        now = datetime.utcnow()

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode.update(
            exp=expire,
            iat=now,
        )

        return jwt.encode(
            payload=to_encode,
            key=private_key,
            algorithm=algorithm,
        )

    @staticmethod
    def decode_jwt(
        token: str | bytes,
        public_key: str = settings.PUBLIC_KEY,
        algorithm: str = settings.ALGORITHM_TYPE,
    ):
        return jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm],
        )


class HashOperations:

    @staticmethod
    def hash_password(password: str):
        return bcrypt.hashpw(
            password=password.encode(),
            salt=bcrypt.gensalt(),
        )

    @staticmethod
    def validate_password(password: str, hashed_password: bytes):
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )


class TokensGenerator:
    TOKEN_TYPE_FIELD: str = "type"
    ACCESS_TOKEN: str = "access token"
    REFRESH_TOKEN: str = "refresh token"

    @staticmethod
    def __generate_token(
        token_data: dict,
        token_type: str = TOKEN_TYPE_FIELD,
        expire_minutes: int = settings.DEFAULT_VALUE_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
    ):
        token_payload = {TokensGenerator.TOKEN_TYPE_FIELD: token_type}
        token_payload.update(token_data)

        return JWTOperations.encode_jwt(
            payload=token_payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta,
        )

    @staticmethod
    def generate_access_token(user: UserSchema):
        payload = {
            "sub": user.username,
            "username": user.username,
            "email": user.email,
        }

        return TokensGenerator.__generate_token(
            token_data=payload,
            token_type=TokensGenerator.ACCESS_TOKEN,
            expire_minutes=5,
        )

    def generate_refresh_token(user: UserSchema):
        payload = {
            "sub": user.username,
        }

        return TokensGenerator.__generate_token(
            token_data=payload,
            token_type=TokensGenerator.REFRESH_TOKEN,
            expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
