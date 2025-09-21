class CannotAllocateError(Exception):
    """
    Raised when an order line cannot be allocated to a batch.

    Attributes:
        orderid: The ID of the order that failed to allocate.
        sku: The SKU of the product that failed to allocate.
        qty: The quantity that could not be allocated.
        message: A detailed error message.
    """

    def __init__(self, orderid: str, sku: str, qty: int, message: str = None):
        """
        Initialize the exception with details about the allocation failure.

        :param orderid: The ID of the order that failed to allocate.
        :param sku: The SKU of the product that failed to allocate.
        :param qty: The quantity that could not be allocated.
        :param message: A custom error message (optional).
        """
        self.orderid = orderid
        self.sku = sku
        self.qty = qty
        self.message = message or f"Cannot allocate {qty} units of SKU '{sku}' for order '{orderid}'."
        super().__init__(self.message)