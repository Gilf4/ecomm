from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import intpk, str255

from .base import Base
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
    attribute_values: Mapped[list['AttributeValue']] = relationship(back_populates='product')
    shopping_cart_items: Mapped[list['ShoppingCartItem']] = relationship(back_populates='product')