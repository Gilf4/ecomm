from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, intpk

class ShoppingCartItem(Base):
    __tablename__ = 'shopping_cart_items'
    
    item_id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey('products.product_id', ondelete='CASCADE'))
    cart_id: Mapped[int] = mapped_column(ForeignKey('shopping_carts.cart_id', ondelete='CASCADE'))
    quantity: Mapped[int]
    
    product: Mapped['Product'] = relationship(back_populates='shopping_cart_items')
    cart: Mapped['ShoppingCart'] = relationship(back_populates='items')