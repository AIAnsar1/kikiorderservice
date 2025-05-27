import uuid
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import Literal, Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, Field, Relationship, Text, Date, DECIMAL, TIMESTAMP
from datetime import datetime, date


class BaseModel(SQLModel):
    pass


class TestModel(BaseModel, table=True):
    __tablename__ = "test_model"
    __table_args__ = {"schema": "public"}

    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4, nullable=False)
    first_name: str = Field(max_length=100, nullable=False)
    last_name: str = Field(max_length=100, nullable=False)
    username: str = Field(max_length=60, nullable=False)
    photo_url: str = Field(nullable=False)
    birth: date = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class TestModelCreate(SQLModel):
    first_name: str
    last_name: str
    username: str
    photo_url: str
    birth: Optional[date] = None


class TestModelUpdate(SQLModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    photo_url: Optional[str]
    birth: Optional[date]


class PaginatedTestResponse(BaseModel):
    data: List[TestModel]
    total: int
    page: int
    per_page: int


# Shared properties
class UserBase(BaseModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(BaseModel):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(BaseModel):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(BaseModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(BaseModel):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
