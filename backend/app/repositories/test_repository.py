from app.model.test_model import TestModel
from app.repositories.base_repository import BaseRepository
from sqlmodel.ext.asyncio.session import AsyncSession





class TestRepository(BaseRepository[TestModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, TestModel)


