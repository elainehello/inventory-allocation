from __future__ import annotations
from typing import Protocol, Optional, Type
from types import TracebackType
from allocation.domain import models

class AbstractProductRepository(Protocol):
    """
    Repository interface for managing Product aggregates.
    """
    def add(self, product: models.Product) -> None: ...
    def get(self, sku: str) -> models.Product | None: ...
    def list(self) -> list[models.Product]: ...

class AbstractUnitOfWork(Protocol):
    """
    Unit of Work interface for managing transactional boundaries.
    """
    products: AbstractProductRepository

    def __enter__(self) -> AbstractUnitOfWork: ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...