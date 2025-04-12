from sqlalchemy.orm import Session
from models import Country
from .base_dao import BaseDAO

class CountryDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Country)
    
    def find_by_name(self, name) -> Country | None:
        """Поиск страны по названию"""
        pass
    
    def get_address_count(self, country_id) -> int:
        """Получение количества адресов в стране"""
        pass