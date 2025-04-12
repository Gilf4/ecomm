from sqlalchemy.orm import Session
from models import ProductCategory
from .base_dao import BaseDAO

class ProductCategoryDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, ProductCategory)
    
    def find_by_name(self, name) -> ProductCategory | None:
        """Поиск категории по названию"""
        return self.session.query(ProductCategory).filter(
            ProductCategory.category_name == name
        ).first()

    def get_or_create_by_name(self, name: str) -> ProductCategory:
        """Возвращает категорию или создает новую."""
        category = self.find_by_name(name)
        if not category:
            category = self.create(category_name=name)
        return category
    
    def get_with_products(self, category_id) -> ProductCategory | None:
        """Получение категории со всеми продуктами"""
        pass