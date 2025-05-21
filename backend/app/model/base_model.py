from __future__ import annotations
from typing import TypeVar, Type
from sqlmodel import Field, Relationship, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload


T = TypeVar("T", bound="BaseModel")

class BaseModel(SQLModel):

    @classmethod
    async def scope_filter(cls: Type[T], session: AsyncSession, data: dict):
        stmt = select(cls)

        if hasattr(cls, "roles"):
            stmt = stmt.options(selectinload(cls.roles))

            if "status" in data:
                stmt = stmt.where(cls.roles.any(status=data["status"]))

            if "roles" in data:
                stmt = stmt.where(cls.roles.any(role_code=data["role"]))

        result = await session.exec(stmt)
        return result.all()

