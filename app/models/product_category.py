from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import intpk, str255

from .base import Base

class ProductCategory(Base):
    __tablename__ = 'product_categories'
    
    category_id: Mapped[intpk]
    category_name: Mapped[str255] = mapped_column(unique=True)
    
    products: Mapped[list['Product']] = relationship(back_populates='category')  # Строковая аннотация