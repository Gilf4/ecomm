from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class UserAddress(Base):
    __tablename__ = 'user_addresses'
    
    address_id: Mapped[int] = mapped_column(ForeignKey('address.address_id', ondelete='CASCADE'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)