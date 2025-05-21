from backend.app.repositories.base_repository import BaseRepository
from app.services.base_service import BaseService
from app.model.base_model import BaseModel
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from typing import AsyncGenerator
from backend.app.repositories.base_repository import BaseRepository
from sqlmodel import SQLModel, Field, text
import pytest_asyncio



class User(BaseModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)



DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine_test = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)




@pytest_asyncio.fixture(scope="module")
async def db() -> AsyncSession:
    async with engine_test.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async with AsyncSessionLocal() as session:
        yield session

    async with engine_test.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)




@pytest.fixture
def user_data():
    return {"name": "John Doe", "email": "john@example.com"}




@pytest.mark.asyncio
async def test_user_service(db, user_data):
    repo = BaseRepository[User](db, User)
    service = BaseService[User](repo)

    created = await service.create(user_data)
    assert created.id is not None

    fetched = await service.get_by_id(created.id)
    assert fetched.id == created.id

    updated = await service.update(created.id, {"name": "Jane"})
    assert updated.name == "Jane"

    deleted = await service.delete(created.id)
    assert deleted.id == created.id

