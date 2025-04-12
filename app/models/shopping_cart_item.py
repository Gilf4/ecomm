from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product
    from .shopping_cart import ShoppingCart

from .base import Base, intpk

class ShoppingCartItem(Base):
    __tablename__ = 'shopping_cart_items'
    
    item_id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey('products.product_id', ondelete='CASCADE'))
    cart_id: Mapped[int] = mapped_column(ForeignKey('shopping_carts.cart_id', ondelete='CASCADE'))
    quantity: Mapped[int]
    
    product: Mapped['Product'] = relationship(back_populates='shopping_cart_items')
    cart: Mapped['ShoppingCart'] = relationship(back_populates='items')

    def __repr__(self):
        return (f"<CartItem(id={self.item_id}, product={self.product.product_name}, "
                f"quantity={self.quantity}, price={self.product.price})>")
