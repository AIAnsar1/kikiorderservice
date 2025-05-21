from fastapi import APIRouter

from app.api.routes import test_route



api_router = APIRouter()
api_router.include_router(test_route.router)






























