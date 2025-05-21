from fastapi import APIRouter, Depends
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from app.model.test_model import TestModel, TestModelCreate, TestModelUpdate, PaginatedTestResponse
from app.repositories.test_repository import TestRepository
from app.services.test_service import TestService
from app.controllers.test_controller import TestController
from app.api.deps import get_db
import uuid

router = APIRouter(prefix="/test", tags=["Test"])

def get_test_repo(db: AsyncSession = Depends(get_db)):
    return TestRepository(db)

def get_test_service(repo: TestRepository = Depends(get_test_repo)):
    return TestService(repo)

def get_test_controller(service: TestService = Depends(get_test_service)):
    return TestController(service)

@router.get("/", response_model=PaginatedTestResponse)
async def list_test(page: int = 1, per_page: int = 10, controller: TestController = Depends(get_test_controller)):
    return controller.list(page=page, per_page=per_page)

@router.get("/{test_id}", response_model=TestModel)
async def get_test(test_id: uuid.UUID, controller: TestController = Depends(get_test_controller)):
    return controller.get(test_id)

@router.post("/", response_model=TestModel)
async def create_test(payload: TestModelCreate, controller: TestController = Depends(get_test_controller)):
    return controller.create(payload)

@router.put("/{test_id}", response_model=TestModel)
async def update_test(test_id: uuid.UUID, payload: TestModelUpdate, controller: TestController = Depends(get_test_controller)):
    return controller.update(test_id, payload)

@router.delete("/{test_id}", response_model=TestModel)
async def delete_test(test_id: uuid.UUID, controller: TestController = Depends(get_test_controller)):
    return controller.delete(test_id)






