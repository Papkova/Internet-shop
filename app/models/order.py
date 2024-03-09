from .base import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)
    items = relationship("Ordered_items", backref="order")


class Ordered_items(Base):
    __tablename__ = "ordered_items"

    id = Column(Integer, primary_key=True)
    oid = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, ForeignKey("carts.quantity"), nullable=False)

