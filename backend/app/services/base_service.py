from typing import Generic, TypeVar, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models import BaseModel



T = TypeVar("T", bound=BaseModel) # по сути сервис работает с репозиторием, а не с моделью напрямую.
# Однако T = TypeVar("T", bound=BaseRepository) в этом случае ограничит тебя на уровне сервиса, что не очень удобно: тебе всё равно нужно знать, с какой моделью работает этот репозиторий.

# Лучше делать так:
# так что ни каких вопросов

# T = TypeVar("T", bound=BaseRepository) # В этом случае не знаешь, какая модель внутри, и теряешь типизацию User, Post, Comment и т.д. — они будут просто частью абстрактного BaseRepository.

class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    def paginated_list(self, page: int = 1, per_page: int = 10, filters: Dict[str, Any] = None, with_relations: list[str] = None) -> Dict[str, Any]:
        return self.repository.paginated_list(page=page, per_page=per_page, filters=filters, with_relations=with_relations)

    def get_by_id(self, id: int) -> T:
        return self.repository.get_by_id(id)

    def create(self, data: dict) -> T:
        return self.repository.create(data)

    def update(self, id: int, data: dict) -> T:
        return self.repository.update(id, data)

    def delete(self, id: int) -> T:
        return self.repository.delete(id)

    def _get_repository(self) -> BaseRepository[T]:
        if not self.repository:
            raise RuntimeError("[ ETA ]: Repository not initialized")
        return self.repository








# kill -9 1457 && kill -9 5361 && kill -9 6360


