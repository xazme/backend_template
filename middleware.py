import time as pizda
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from jwt.exceptions import ExpiredSignatureError
from starlette.responses import Response
from app.auth import ExcHelper, JWTOperations, TokensGenerator
from validators import oauth2_access_scheme, TokenService, UserService


class TestMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            token = await oauth2_access_scheme(request=request)
        except Exception:
            await call_next(request)

        try:
            payload = JWTOperations.decode_jwt(token=token)
            TokenService.validate_token(
                payload=payload, selected_token=TokensGenerator.ACCESS_TOKEN
            )
        except ExpiredSignatureError:
            return ExcHelper.raise_http_401_not_auth(detail="Token has expired")
        except Exception:
            return ExcHelper.raise_http_403_forbiden(detail="Invalid token")

        user = UserService.get_user_from_database(payload=payload)
        request.state.user = user
        return await call_next(request)
