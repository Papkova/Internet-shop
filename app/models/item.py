from .base import Base
from sqlalchemy import Column, String, Integer, Text, Float
from sqlalchemy.orm import relationship


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(Text(250), nullable=False)
    image = Column(String(250), nullable=False)
    details = Column(String(250), nullable=False)
    price_id = Column(String(250), nullable=False)
    orders = relationship("Ordered_items", backref="item")
    in_cart = relationship("Cart", backref="item")