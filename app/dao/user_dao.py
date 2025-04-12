from sqlalchemy.orm import Session, joinedload
from models import User
from .base_dao import BaseDAO
from models import ShoppingCart
from models import ShoppingCartItem

class UserDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, User)
    
    def find_by_email(self, email) -> User | None:
        """Поиск по email"""
        return self.session.query(User).filter(User.email == email).first()

    
    def get_with_cart(self, user_id) -> User | None:
        """Получение пользователя с корзиной"""
        return self.session.query(User).options(
            joinedload(User.shopping_carts)  # Жадная загрузка корзин
            .joinedload(ShoppingCart.items)  # Загрузка элементов корзины
            .joinedload(ShoppingCartItem.product)  # Загрузка связанных продуктов
        ).get(user_id)
    
    def add_address(self, user_id, address_id) -> None:
        """Добавление адреса пользователю"""
        pass
    
    def remove_address(self, user_id, address_id) -> None:
        """Удаление адреса у пользователя"""
        pass
