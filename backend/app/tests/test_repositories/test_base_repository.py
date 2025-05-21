import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from typing import AsyncGenerator
from backend.app.repositories.base_repository import BaseRepository
from backend.app.model.base_model import BaseModel
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
async def test_create_user(db, user_data):
    repo = BaseRepository[User](db, User)
    user = await repo.create(user_data)
    assert user.id is not None
    assert user.name == "John Doe"
    assert user.email == "john@example.com"


@pytest.mark.asyncio
async def test_get_by_id(db, user_data):
    repo = BaseRepository[User](db, User)
    user = await repo.create(user_data)
    found = await repo.get_by_id(user.id)
    assert found is not None
    assert found.id == user.id


@pytest.mark.asyncio
async def test_update_user(db, user_data):
    repo = BaseRepository[User](db, User)
    user = await repo.create(user_data)
    updated = await repo.update(user.id, {"name": "Jane"})
    assert updated.name == "Jane"


@pytest.mark.asyncio
async def test_delete_user(db, user_data):
    repo = BaseRepository[User](db, User)
    user = await repo.create(user_data)
    deleted = await repo.delete(user.id)
    assert deleted.id == user.id
    should_be_none = await repo.get_by_id(user.id)
    assert should_be_none is None



@pytest.mark.asyncio
async def test_paginated_list(db, user_data):
    repo = BaseRepository[User](db, User)

    for i in range(15):
        await repo.create({"name": f"User{i}", "email": f"user{i}@example.com"})
    result = await repo.paginated_list(page=2, per_page=5)
    assert result["page"] == 2
    assert result["per_page"] == 5
    assert len(result["data"]) == 5
    assert result["total"] >= 15











