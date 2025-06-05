from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils
from app.core.config import settings
from app.api.routes.orders import router as orders_router
from app.api.routes.status import router as status_router

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(orders_router)
api_router.include_router(status_router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
