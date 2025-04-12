from abc import ABC, abstractmethod
from models import Product
from dao import ProductDAO, ProductCategoryDAO

class Builder(ABC):
    @abstractmethod
    def with_name(self, name):
        pass

    @abstractmethod
    def with_price(self, price):
        pass

    @abstractmethod
    def with_category(self, category_name):
        pass

    @abstractmethod
    def with_attribute(self, name, value):
        pass

    @abstractmethod
    def build(self):
        pass

class ProductBuilder(Builder):
    def __init__(self, session):
        self.session = session
        self.reset()

    def reset(self):
        self._product_data = {
            'product_name': None,
            'price': None,
            'category_name': None,
            'product_description': None,
            'product_img': None
        }
        self._attributes: dict[str, str] = {}

    def with_name(self, name):
        self._product_data['product_name'] = name
        return self

    def with_price(self, price):
        self._product_data['price'] = price
        return self

    def with_category(self, category_name):
        self._product_data['category_name'] = category_name
        return self
    
    def with_description(self, description: str):
        self._product_data['product_description'] = description
        return self

    def with_attribute(self, name, value):
        self._attributes[name] = value
        return self

    def build(self) -> Product:
        category = ProductCategoryDAO(self.session).get_or_create_by_name(
            self._product_data['category_name']
        )

        product = ProductDAO(self.session).create(
            product_name=self._product_data['product_name'],
            price=self._product_data['price'],
            category_id=category.category_id,
            product_description=self._product_data['product_description'],
            product_img=self._product_data['product_img']
        )
        
        for name, value in self._attributes.items():
            ProductDAO(self.session).add_attribute(
                product.product_id,
                name,
                value
            )
        
        return product