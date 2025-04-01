from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, intpk, str255

class Attribute(Base):
    __tablename__ = 'attributes'
    
    attribute_id: Mapped[intpk]
    attribute_name: Mapped[str255] = mapped_column(unique=True)
    
    values: Mapped[list['AttributeValue']] = relationship(back_populates='attribute')