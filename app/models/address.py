from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, intpk, str255

class Address(Base):
    __tablename__ = 'address'
    
    address_id: Mapped[intpk]
    city: Mapped[str255]
    street: Mapped[str255]
    house: Mapped[str] = mapped_column(String(50))
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.country_id', ondelete='CASCADE'))
    
    country: Mapped['Country'] = relationship(back_populates='addresses')
    users: Mapped[list['User']] = relationship(secondary='user_addresses', back_populates='addresses')