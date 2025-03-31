from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Attribute(Base):
    __tablename__ = 'attributes'
    
    attribute_id: Mapped[int] = mapped_column(primary_key=True)
    attribute_name: Mapped[str] = mapped_column(String(255), unique=True)
    
    values: Mapped[list['AttributeValue']] = relationship(back_populates='attribute')