from .base import Base, session
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from .cart import Cart


class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(30), nullable=False, unique=True)
    password = Column(String(250), nullable=False, unique=True)
    admin = Column(Boolean, default=False, nullable=False)
    email_confirmed = Column(Boolean, nullable=True, default=False)
    cart = relationship("Cart", backref="buyer")
    orders = relationship("Order", backref="customer")

    def add_to_cart(self, item_id, quantity):
        item_to_add = session.query(Cart).filter_by(item_id=item_id, quantity=quantity, uid=self.id)
        try:
            session.add(item_to_add)
            session.commit()
        except Exception as exc:
            return exc
        finally:
            session.close()

    def remove_from_cart(self, item_id, quantity):
        item_to_delete = session.query(Cart).filter_by(item_id=item_id, quantity=quantity, uid=self.id).first()
        try:
            session.delete(item_to_delete)
            session.commit()
        except Exception as exc:
            return exc
        finally:
            session.close()

