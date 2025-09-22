from allocation.domain import models, commands
from allocation.service_layer.ports import AbstractUnitOfWork
from allocation.domain.exceptions import CannotAllocateError

class InvalidSku(Exception):
    """Application-level exception for non-existent SKUs."""
    pass

def add_batch(command: commands.CreateBatch, uow: AbstractUnitOfWork):
    """
    Handle the CreateBatch command by adding a new batch to the repository.
    """
    with uow:
        product = uow.products.get(sku=command.sku)
        if product is None:
            product = models.Product(sku=command.sku, batches=[])
            uow.products.add(product)
        
        product.batches.append(models.Batch(
            ref=command.ref,
            sku=command.sku,
            purchased_qty=command.qty,
            eta=command.eta
        ))
        uow.commit()

def allocate(command: commands.Allocate, uow: AbstractUnitOfWork):
    """
    Handle the Allocate command by allocating an order line to a batch.
    """
    line = models.OrderLine(command.orderid, command.sku, command.qty)
    with uow:
        product = uow.products.get(sku=command.sku)
        if product is None:
            raise InvalidSku(f"Invalid SKU {command.sku}")
        
        try:
            batchref = product.allocate(line)
            uow.commit()
            return batchref
        except CannotAllocateError:
            raise  # Bubble up the domain exception for higher-level handling

def change_batch_quantity(command: commands.ChangeBatchQuantity, uow: AbstractUnitOfWork):
    """
    Handle the ChangeBatchQuantity command by updating the quantity of a batch.
    """
    with uow:
        product = uow.products.get_by_batchref(command.ref)
        if product is None:
            raise InvalidSku(f"Invalid batch reference {command.ref}")
        
        # Delegate the logic to the Product aggregate
        product.change_batch_quantity(ref=command.ref, qty=command.qty)
        uow.commit()

