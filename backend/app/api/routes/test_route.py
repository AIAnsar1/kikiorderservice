from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import TestModel, TestModelCreate, TestModelUpdate, PaginatedTestResponse
from app.repositories.test_repository import TestRepository
from app.services.test_service import TestService
from app.api.deps import get_db
import uuid

router = APIRouter(prefix="/test", tags=["Test"])

def get_test_repo(db: AsyncSession = Depends(get_db)):
    return TestRepository(db)

def get_test_service(repo: TestRepository = Depends(get_test_repo)):
    return TestService(repo)

@router.get("/", response_model=PaginatedTestResponse)
async def list_test(page: int = 1, per_page: int = 10, service: TestService = Depends(get_test_service)):
    return service.paginated_list(page=page, per_page=per_page)

@router.get("/{test_id}", response_model=TestModel)
async def get_test(test_id: uuid.UUID, service: TestService = Depends(get_test_service)):
    obj = service.get_by_id(test_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not Found")
    return obj

@router.post("/", response_model=TestModel)
async def create_test(payload: TestModelCreate, service: TestService = Depends(get_test_service)):
    return service.create(payload.dict())

@router.put("/{test_id}", response_model=TestModel)
async def update_test(test_id: uuid.UUID, payload: TestModelUpdate, service: TestService = Depends(get_test_service)):
    updated_obj = service.update(test_id, payload.dict(exclude_unset=True))
    if not updated_obj:
        raise HTTPException(status_code=404, detail="Not Found")
    return updated_obj

@router.delete("/{test_id}", response_model=TestModel)
async def delete_test(test_id: uuid.UUID, service: TestService = Depends(get_test_service)):
    deleted_obj = service.delete(test_id)
    if not deleted_obj:
        raise HTTPException(status_code=404, detail="Not Found")
    return deleted_obj