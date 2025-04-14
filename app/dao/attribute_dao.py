from sqlalchemy.orm import Session
from models import Attribute
from .base_dao import BaseDAO

class AttributeDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Attribute)
    
    def find_by_name(self, name) -> Attribute:
        """Поиск атрибута по названию"""
        return self.session.query(Attribute).filter(
            Attribute.attribute_name == name
        ).first()
