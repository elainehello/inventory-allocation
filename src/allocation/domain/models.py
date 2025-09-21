from dataclasses import dataclass
from typing import Set, List, Optional
from datetime import timedelta, date

from .exceptions import CannotAllocateError
from .events import BatchAllocated, OutOfStock

# ------------------------------
# 1. VALUE OBJECT
# ------------------------------

@dataclass(frozen=True)
class OrderLine:
    """
    Represents an order line as a Value Object.
    Immutable and equality is based on its data.
    """
    orderid: str  # Unique identifier for the order
    sku: str      # Stock Keeping Unit (product identifier)
    qty: int      # Quantity of the product in the order


# ------------------------------
# 2. ENTITY
# ------------------------------

class Batch:
    """
    Represents a batch of products (Entity).
    Tracks allocations, ensures business invariants, and records domain events.
    """
    def __init__(self, ref: str, sku: str, purchased_qty: int, eta: Optional[timedelta] = None):
        """
        Initialize a Batch instance.

        :param ref: Unique reference for the batch (identity of the entity).
        :param sku: Stock Keeping Unit (product identifier) for the batch.
        :param purchased_qty: Total quantity purchased in this batch.
        :param eta: Estimated time of arrival for the batch (optional).
        """
        self.reference = ref  # Unique identifier for the batch
        self.sku = sku  # SKU of the product in this batch
        self.eta = eta  # Estimated time of arrival (optional)
        self._purchased_quantity = purchased_qty  # Total quantity purchased
        self._allocations: Set[OrderLine] = set()  # Set of allocated order lines
        self.events: List[object] = []  # List of domain events triggered by this batch

    def __eq__(self, other: object) -> bool:
        """
        Check equality based on the batch reference.
        """
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        """
        Hash the batch based on its reference.
        """
        return hash(self.reference)

    @property
    def allocated_qty(self) -> int:
        """
        Total quantity allocated to this batch.
        """
        return sum(line.qty for line in self._allocations)

    @property
    def available_qty(self) -> int:
        """
        Quantity available for allocation.
        """
        return self._purchased_quantity - self.allocated_qty

    def can_allocate(self, line: OrderLine) -> bool:
        """
        Check if the batch can allocate the given order line.

        :param line: The order line to check.
        :return: True if the batch can allocate the order line, False otherwise.
        """
        return self.sku == line.sku and self.available_qty >= line.qty

    def allocate(self, line: OrderLine):
        """
        Allocate an order line to this batch.

        :param line: The order line to allocate.
        :raises CannotAllocateError: If the batch cannot allocate the order line.
        """
        if not self.can_allocate(line):
            raise CannotAllocateError(
                f"Batch {self.reference} cannot allocate {line.qty} units of {line.sku}."
            )

        if line in self._allocations:
            # Allocation is idempotent; if already allocated, do nothing.
            return

        # Add the order line to the allocations
        self._allocations.add(line)

        # Record a domain event for the allocation
        self.events.append(BatchAllocated(
            orderid=line.orderid,
            sku=line.sku,
            qty=line.qty,
            batchref=self.reference
        ))

        # Trigger an OutOfStock event if no stock is left
        if self.available_qty == 0:
            self.events.append(OutOfStock(sku=self.sku))

    def deallocate(self, line: OrderLine):
        """
        Remove an allocation for the given order line.

        :param line: The order line to deallocate.
        """
        if line in self._allocations:
            # Remove the order line from the allocations
            self._allocations.remove(line)
            # Optionally, you could emit a domain event for deallocation


# ------------------------------
# 3. AGGREGATE ROOT
# ------------------------------

class Product:
    """
    Represents a Product aggregate, which manages multiple batches of stock.
    The Product is the aggregate root, ensuring consistency across its batches.
    """
    def __init__(self, sku: str, batches: List[Batch]):
        """
        Initialize a Product instance.

        :param sku: Stock Keeping Unit (product identifier) for the product.
        :param batches: List of batches associated with this product.
        """
        self.sku = sku
        self.batches = batches

    def allocate(self, line: OrderLine) -> Optional[str]:
        """
        Allocate an order line to one of the product's batches.

        :param line: The order line to allocate.
        :return: The reference of the batch to which the order line was allocated.
        :raises CannotAllocateError: If the order line cannot be allocated.
        """
        if line.sku != self.sku:
            raise CannotAllocateError(f"SKU mismatch: {line.sku} not in product {self.sku}")
        
        # Business rule: prefer batches with the earliest ETA
        sorted_batches = sorted(self.batches, key=lambda b: b.eta or date.min)
        
        for batch in sorted_batches:
            if batch.can_allocate(line):
                batch.allocate(line)
                return batch.reference
        
        # If no batch can allocate, raise an error
        raise CannotAllocateError(f"Out of stock for {line.sku}")