from app.models import TestModel
from app.repositories.test_repository import TestRepository
from app.services.base_service import BaseService





class TestService(BaseService[TestModel]):
    def __init__(self, repository: TestRepository):
        super().__init__(repository)







































