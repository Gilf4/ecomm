from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import intpk, str255

from .base import Base
from .address import Address

class User(Base):
    __tablename__ = 'users'
    
    user_id: Mapped[intpk]
    email: Mapped[str255] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(Text())
    first_name: Mapped[str255]
    last_name: Mapped[str255]
    phone_number: Mapped[str | None] = mapped_column(String(20))
    
    addresses: Mapped[list['Address']] = relationship(secondary='user_addresses', back_populates='users')
    shopping_carts: Mapped[list['ShoppingCart']] = relationship(back_populates='user')