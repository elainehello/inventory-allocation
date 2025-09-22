from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

@dataclass
class Command:
    """
    Base class for all commands.
    """
    pass

@dataclass
class CreateBatch(Command):
    """
    Command to create a new batch of stock.
    """
    ref: str
    sku: str
    qty: int
    eta: Optional[timedelta] = None

@dataclass
class Allocate(Command):
    """
    Command to allocate an order line to a batch.
    """
    orderid: str
    sku: str
    qty: int

@dataclass
class ChangeBatchQuantity(Command):
    """
    Command to change the quantity of a batch.
    """
    ref: str
    qty: int