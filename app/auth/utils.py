import jwt
import bcrypt
from app.config import settings
from datetime import timedelta, datetime
from fastapi import HTTPException, status

from schm_test import UserSchema


class ExcHelper:
    @staticmethod
    def raise_http_401_not_auth(detail: str = "not auth"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    @staticmethod
    def raise_http_403_forbiden(detail: str = "forbiden"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class JWTHelper:

    @staticmethod
    def encode_jwt(
        payload: dict,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        private_key: str = settings.PRIVATE_KEY,
        algorithm: str = settings.ALGORITHM_TYPE,
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

        token = jwt.encode(
            payload=to_encode,
            key=private_key,
            algorithm=algorithm,
        )

        return token

    @staticmethod
    def decode_jwt(
        token: str | bytes,
        public_key: str = settings.PUBLIC_KEY,
        algorithm: str = settings.ALGORITHM_TYPE,
    ):
        try:
            payload = jwt.decode(
                jwt=token,
                key=public_key,
                algorithms=[algorithm],
            )
        except jwt.InvalidTokenError:
            raise ExcHelper.raise_http_401_not_auth(detail="invalid token")

        return payload


class HashHelper:

    @staticmethod
    def check_password(password: str, hashed_password: bytes):
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed_password
        )

    @staticmethod
    def hash_password(password: str):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=password.encode(), salt=salt)
        return hashed_password


class JWTMaker:

    TOKEN_TYPE_FIELD = "type"
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"

    @staticmethod
    def create_token(
        token_data: dict,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: datetime | None = None,
        token_type=TOKEN_TYPE_FIELD,
    ):
        jwt_payload = {JWTMaker.TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)

        return JWTHelper.encode_jwt(
            payload=jwt_payload,
            expire_timedelta=expire_timedelta,
            expire_minutes=expire_minutes,
        )

    @staticmethod
    def generate_access_token(user: UserSchema):
        payload = {
            "username": user.username,
            "email": user.email,
        }
        token = JWTMaker.create_token(
            token_data=payload,
            token_type=JWTMaker.ACCESS_TOKEN,
        )
        return token

    @staticmethod
    def generate_refresh_token(user: UserSchema):
        payload = {
            "username": user.username,
        }

        token = JWTMaker.create_token(
            token_data=payload,
            token_type=JWTMaker.REFRESH_TOKEN,
            expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return token
