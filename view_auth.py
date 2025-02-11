from datetime import datetime
import secrets
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from typing import Annotated

router = APIRouter(prefix="/demo-auth", tags=["AUTH DEMO"])

security = HTTPBasic(auto_error=False)


tokens_to_users = {
    "zxcad71y42ikjdad": "admin",
    "t7iyouwajkdmsn": "CHINAAZES",
}

COOKIES: dict[str, dict[str, any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


def get_auth_by_token(static_token: Annotated[str, Header(alias="token")]):
    if username := tokens_to_users.get(static_token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
    )


def generate_session_id():
    return uuid4().hex


def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)):
    if session_id not in COOKIES:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not auth")
    return COOKIES[session_id]


@router.get("/cookie-auth-username/")
async def demo_auth_set_cookie(
    response: Response,
    auth_username: str = Depends(get_auth_by_token),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {"username": auth_username, "login at": datetime.now()}
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"msg": "okey succes auth"}


@router.get("/check-cookie/")
async def demo_auth_check_cookie(user_session_data: dict = Depends(get_session_data)):
    username = user_session_data["username"]
    return {
        "msg": username,
        **user_session_data,
    }


@router.get("/logout-cookie/")
async def demo_auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {"msg": f"bye {username}"}
