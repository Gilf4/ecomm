from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class ProductCategory(Base):
    __tablename__ = 'product_categories'
    
    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(255), unique=True)
    
    products: Mapped[list['Product']] = relationship(back_populates='category')  # Строковая аннотация