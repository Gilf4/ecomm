from sqlalchemy.orm import Session

from .base_dao import BaseDAO
from models import AttributeValue

class AttributeValueDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, AttributeValue)
    
    def get_for_product(self, product_id) -> list[AttributeValue]:
        """Получение всех значений для конкретного продукта"""
        return self.session.query(AttributeValue).filter(
            AttributeValue.product_id == product_id
        ).all()
    
    def get_for_attribute(self, attribute_id) -> list[AttributeValue]:
        """Получение всех значений для конкретного атрибута"""
        pass
    
    def get_by_product_and_attribute(self, product_id, attribute_id) -> AttributeValue | None:
        """Поиск конкретного значения атрибута для продукта"""
        pass