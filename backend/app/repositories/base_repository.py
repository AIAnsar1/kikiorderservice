from typing import Generic, TypeVar, Type, Optional, Dict, Any, List
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql import ColumnElement
from sqlalchemy.exc import NoResultFound
from app.model.base_model import BaseModel
import uuid

T = TypeVar("T", bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    def paginated_list(self,page: int = 1,per_page: int = 10,filters: Optional[Dict[str, Any]] = None,with_relations: Optional[List[str]] = None) -> Dict[str, Any]:
        stmt = select(self.model)

        if with_relations:
            for relation in with_relations:
                stmt = stmt.options(joinedload(relation))

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    stmt = stmt.where(getattr(self.model, key) == value)
        stmt = stmt.order_by(self.model.id.desc())
        result = self.db.execute(stmt)
        total = result.scalars().unique().all()
        items = total[(page - 1) * per_page: page * per_page]
        return {"data": items, "total": len(total), "page": page, "per_page": per_page}

    def get_by_id(self, id: uuid.UUID, with_relations: Optional[List[str]] = None) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == id)

        if with_relations:
            for relation in with_relations:
                stmt = stmt.options(joinedload(relation))
        result = self.db.execute(stmt)
        return result.scalars().first()

    def create(self, data: dict) -> T:
        obj = self.model(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id: uuid.UUID, data: dict) -> Optional[T]:
        obj = self.get_by_id(id)

        if not obj:
            return None

        for key, value in data.items():
            setattr(obj, key, value)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: uuid.UUID) -> Optional[T]:
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj

    def _query(self):
        stmt = select(self.model).order_by(self.model.id.desc())
        result = self.db.execute(stmt)
        return result.all()

    def find_by_one(self, field: str, value: Any) -> Optional[T]:
        column: ColumnElement = getattr(self.model, field)
        stmt = select(self.model).where(column == value)
        result = self.db.execute(stmt)
        return result.scalars().first()

    def _get_model(self):
        return self.model