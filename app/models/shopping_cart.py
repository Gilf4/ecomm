from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from user import User
    from .shopping_cart_item import ShoppingCartItem

from .base import Base, intpk

class ShoppingCart(Base):
    __tablename__ = 'shopping_carts'
    
    cart_id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    
    user: Mapped['User'] = relationship(back_populates='shopping_carts')
    items: Mapped[list['ShoppingCartItem']] = relationship(back_populates='cart')