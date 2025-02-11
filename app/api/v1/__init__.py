from fastapi import APIRouter

# from .user_routes import router as users_router

#
from view_auth import router as auth_router
from demo_jwt import router as jwt_auth_router

router = APIRouter()
router.include_router(router=auth_router)
router.include_router(router=jwt_auth_router)
# router.include_router(router=users_router)
