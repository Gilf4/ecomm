from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Address(Base):
    __tablename__ = 'address'
    
    address_id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(255))
    street: Mapped[str] = mapped_column(String(255))
    house: Mapped[str] = mapped_column(String(50))
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.country_id', ondelete='CASCADE'))
    
    country: Mapped['Country'] = relationship(back_populates='addresses')
    users: Mapped[list['User']] = relationship(secondary='user_addresses', back_populates='addresses')