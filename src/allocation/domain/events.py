from dataclasses import dataclass

# ------------------------------
# 1. DOMAIN EVENTS
# ------------------------------
# Domain events are immutable data structures that represent significant
# occurrences in the domain. They are used to notify other parts of the
# system about changes in the state of the domain.

@dataclass(frozen=True)
class BatchAllocated:
    """
    Event triggered when an order line is successfully allocated to a batch.
    """
    orderid: str
    sku: str
    qty: int
    batchref: str


@dataclass(frozen=True)
class OutOfStock:
    """
    Event triggered when a batch runs out of stock for a specific SKU.
    """
    sku: str
