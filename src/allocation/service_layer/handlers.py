from allocation.domain import models
from allocation.service_layer.ports import AbstractUnitOfWork
from allocation.domain.exceptions import CannotAllocateError

class InvalidSku(Exception):
    """Application-level exception for non-existent SKUs."""
    pass

def allocate_order_handler(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork):
    """
    Orchestrates the allocation use case:
    1. Wrap in UoW (transactional boundary).
    2. Fetch aggregate root (Product).
    3. Delegate business rules to the domain (Product.allocate).
    4. Commit if successful, raise errors otherwise.
    """
    line = models.OrderLine(orderid, sku, qty)

    with uow:
        product = uow.products.get(sku=sku)

        if product is None:
            raise InvalidSku(f"Invalid SKU {sku}")

        try:
            batchref = product.allocate(line)  # domain logic
        except CannotAllocateError:
            raise  # bubble up domain exception (e.g., for API translation)
        
        uow.commit()
        return batchref

