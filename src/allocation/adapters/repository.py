from sqlalchemy.orm import selectinload, Session, Query
from allocation.domain import models
from allocation.service_layer.ports import AbstractProductRepository

class SqlAlchemyProductRepository(AbstractProductRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def add(self, product: models.Product) -> None:
        self.session.add(product)

    def get(self, sku: str) -> models.Product | None:
        query: Query[models.Product] = (
            self.session.query(models.Product)
            .filter_by(sku=sku)
            .options(selectinload(models.Product.batches))
        )
        return query.first()