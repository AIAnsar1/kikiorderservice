from fastapi import APIRouter, Depends, HTTPException
from typing import List, Type, Generic, TypeVar, Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from app.controllers.base_controller import BaseController
from app.model.base_model import BaseModel
from app.model.test_model import TestModel, TestModelCreate, TestModelUpdate
from app.services.base_service import BaseService
from app.api.deps import get_db
from app.services.test_service import TestService




class TestController(BaseController[TestModel, TestModelCreate, TestModelUpdate]):
    def __init__(self, service: TestService):
        super().__init__(service)































































































