import jwt
import bcrypt
from datetime import datetime, timedelta
from app.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.PRIVATE_KEY,
    algorithm: str = settings.ALGORITHM_TYPE,
    expire_minutes: int = settings.access_token_expire_minutes,
):
    to_encode = payload.copy()
    now = datetime.now()
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )

    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.PUBLIC_KEY,
    algorithm: str = settings.ALGORITHM_TYPE,
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )

    return decoded


def hash_pswrd(
    password: str,
):
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
):
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
