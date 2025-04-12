from sqlalchemy import ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product_category import ProductCategory
    from .attribute_value import AttributeValue

from .base import Base, intpk, str255
from .shopping_cart_item import ShoppingCartItem

class Product(Base):
    __tablename__ = 'products'
    
    product_id: Mapped[intpk]
    category_id: Mapped[int] = mapped_column(ForeignKey('product_categories.category_id', ondelete='CASCADE'))
    product_name: Mapped[str255]
    product_description: Mapped[str | None] = mapped_column(Text())
    product_img: Mapped[str | None] = mapped_column(Text())
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    
    category: Mapped['ProductCategory'] = relationship(back_populates='products')
    attribute_values: Mapped[list['AttributeValue']] = relationship(back_populates='product', cascade="all, delete-orphan")
    shopping_cart_items: Mapped[list['ShoppingCartItem']] = relationship(back_populates='product')

    def __repr__(self):
        return f"<Product(id={self.product_id}, name='{self.product_name}', price={self.price})>"
