from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product

from .base import Base, intpk, str255

class ProductCategory(Base):
    __tablename__ = 'product_categories'
    
    category_id: Mapped[intpk]
    category_name: Mapped[str255] = mapped_column(unique=True)
    
    products: Mapped[list['Product']] = relationship(back_populates='category')