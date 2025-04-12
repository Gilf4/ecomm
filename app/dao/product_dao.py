from sqlalchemy.orm import Session
from models import Product, AttributeValue
from .base_dao import BaseDAO
from .attribute_value_dao import AttributeValueDAO
from .attribute_dao import AttributeDAO
from .product_category_dao import ProductCategoryDAO

class ProductDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, Product)
    
    def search_by_name(self, name_part) -> list[Product]:
        """Поиск продуктов по названию"""
        return self.session.query(Product).filter(
            Product.product_name.ilike(f"%{name_part}%")
        ).all()

    def add_attribute(self, product_id, attribute_name, value) -> AttributeValue:
        """Добавление атрибута продукту"""
        attribute = AttributeDAO(self.session).find_by_name(attribute_name)
        if not attribute:
            attribute = AttributeDAO(self.session).create(attribute_name=attribute_name)
        
        return AttributeValueDAO(self.session).create(
            product_id=product_id,
            attribute_id=attribute.attribute_id,
            value=value
        )
    
    def get_attributes(self, product_id) -> dict[str, str]:
        """Получение всех атрибутов продукта в виде словаря"""
        values = AttributeValueDAO(self.session).get_for_product(product_id)
        return {val.attribute.attribute_name: val.value for val in values}
    
    def create_with_category(self, product_name: str, price: float, category_name: str, **kwargs) -> Product:
        """
        Создает продукт с категорией по имени.
        Если категория не существует - создает ее.
        """
        category_dao = ProductCategoryDAO(self.session)
        category, _ = category_dao.get_or_create_by_name(category_name)
        
        return self.create(
            product_name=product_name,
            price=price,
            category_id=category.category_id,
            **kwargs
        )
    
    def get_by_category(self, category_id) -> list[Product]:
        """Фильтрация по категории"""
        pass
    
    def get_by_price_range(self, min_price, max_price) -> list[Product]:
        """Фильтрация по диапазону цен"""
        pass
    
    def get_with_attributes(self, product_id) -> Product | None:
        """Получение продукта со всеми атрибутами"""
        pass
