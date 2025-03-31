from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .attribute import Attribute
from .product import Product

class AttributeValue(Base):
    __tablename__ = 'attribute_values'
    
    value_id: Mapped[int] = mapped_column(primary_key=True)
    attribute_id: Mapped[int] = mapped_column(ForeignKey('attributes.attribute_id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.product_id', ondelete='CASCADE'))
    value: Mapped[str] = mapped_column(Text())
    
    attribute: Mapped['Attribute'] = relationship(back_populates='values')
    product: Mapped['Product'] = relationship(back_populates='attribute_values')