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
    
    def delete_by_product(self, product_id):
        """Удаляет все атрибуты продукта. Возвращает количество удаленных."""
        count = self.session.query(AttributeValue).filter(AttributeValue.product_id == product_id).delete()
        return count