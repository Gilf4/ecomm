from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .address import Address

from .base import Base, intpk, str255


class Country(Base):
    __tablename__ = 'countries'
        
    country_id: Mapped[intpk]
    country_name: Mapped[str255] = mapped_column(unique=True)
    
    addresses: Mapped[list['Address']] = relationship(back_populates='country')