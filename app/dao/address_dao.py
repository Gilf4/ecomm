from models import Address
from sqlalchemy.orm import Session
from .base_dao import BaseDAO

class AddressDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Address)
    
    def get_by_country(self, country_id) -> list[Address]:
        pass

    def find_by_city(self, city) -> list[Address]:
        pass
    
