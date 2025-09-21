from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, MetaData
from sqlalchemy.orm import relationship, registry
from allocation.domain import models

metadata = MetaData()

order_lines = Table(
    "order_lines", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderid", String(255)),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
)

batches = Table(
    "batches", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255), ForeignKey("products.sku")),
    Column("purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", Integer, ForeignKey("order_lines.id")),
    Column("batch_id", Integer, ForeignKey("batches.id")),
)

products = Table(
    "products", metadata,
    Column("sku", String(255), primary_key=True),
    Column("version_number", Integer, nullable=False, default=1),
)
mapper_registry = registry()

def start_mappers():
    mapper_registry.map_imperatively(models.OrderLine, order_lines)

    mapper_registry.map_imperatively(models.Batch, batches, properties={
        "_allocations": relationship(
            models.OrderLine,
            secondary=allocations,
            collection_class=set,
        ),
        "_purchased_quantity": batches.c.purchased_quantity,
    })

    mapper_registry.map_imperatively(models.Product, products, properties={
        "batches": relationship(models.Batch, collection_class=list),
        "version_number": products.c.version_number,
    })