from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, intpk, str255

class Country(Base):
    __tablename__ = 'countries'
        
    country_id: Mapped[intpk]
    country_name: Mapped[str255] = mapped_column(unique=True)
    
    addresses: Mapped[list['Address']] = relationship(back_populates='country')