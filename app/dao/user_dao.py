from sqlalchemy.orm import Session, joinedload
from models import User
from .base_dao import BaseDAO
from models import ShoppingCart
from models import ShoppingCartItem

class UserDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, User)
    
    def find_by_email(self, email) -> User:
        """Поиск по email"""
        return self.session.query(User).filter(User.email == email).first()
    
    def get_with_cart(self, user_id) -> User:
        """Получение пользователя с корзиной"""
        return self.session.query(User).options(
            joinedload(User.shopping_carts)
            .joinedload(ShoppingCart.items)
            .joinedload(ShoppingCartItem.product)
        ).get(user_id)
    
    def authenticate(self, email, password) -> User:
        user = self.find_by_email(email)
        if user and user.password_hash == password:
            return user
        return None
