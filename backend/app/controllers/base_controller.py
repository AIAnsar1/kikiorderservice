from fastapi import APIRouter, Depends, HTTPException
from typing import List, Type, Generic, TypeVar, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.base_service import BaseService
from app.model.base_model import BaseModel
from app.api.deps import get_db
import uuid

T = TypeVar("T", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseController(Generic[T, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, service: BaseService[T]):
        self.service = service

    def list(self, page: int = 1, per_page: int = 10):
        filters = {}
        return self.service.paginated_list(page=page, per_page=per_page, filters=filters)

    def get(self, id: uuid.UUID):
        obj = self.service.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not Found")
        return obj

    def create(self, obj_in: CreateSchemaType):
        return self.service.create(obj_in.dict())

    def update(self, id: uuid.UUID, obj_in: UpdateSchemaType):
        updated_obj = self.service.update(id, obj_in.dict(exclude_unset=True))
        if not updated_obj:
            raise HTTPException(status_code=404, detail="Not Found")
        return updated_obj

    def delete(self, id: uuid.UUID):
        deleted_obj = self.service.delete(id)
        if not deleted_obj:
            raise HTTPException(status_code=404, detail="Not Found")
        return deleted_obj


















































