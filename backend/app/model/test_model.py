from __future__ import annotations
import uuid
from typing import Literal, Optional, List
from sqlmodel import SQLModel, Field, Relationship, Text, Date, DECIMAL, TIMESTAMP
from datetime import datetime, date
from .base_model import BaseModel

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































