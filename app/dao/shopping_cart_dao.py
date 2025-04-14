from sqlalchemy.orm import Session, joinedload
from models import ShoppingCart, ShoppingCartItem
from .base_dao import BaseDAO
from .shopping_cart_item_dao import ShoppingCartItemDAO

class ShoppingCartDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, ShoppingCart)
    
    def get_user_cart(self, user_id) -> ShoppingCart:
        """Получает корзину пользователя со всеми товарами"""
        return self.session.query(ShoppingCart).options(
            joinedload(ShoppingCart.items)
            .joinedload(ShoppingCartItem.product)
        ).filter(
            ShoppingCart.user_id == user_id
        ).first()
    
    def add_to_cart(self, user_id, product_id) -> ShoppingCartItem:
        """Добавления товара в корзину"""
        cart = self.get_user_cart(user_id)
        
        if not cart:
            cart = self.create(user_id=user_id)
        
        item_dao = ShoppingCartItemDAO(self.session)
        item = item_dao.find_item(cart.cart_id, product_id)
        
        if item:
            item_dao.increase_quantity(item.item_id)
        else:
            item = item_dao.add_item(cart.cart_id, product_id)
        
        return item
    
    def calculate_total(self, cart_id):
        """Расчет общей стоимости корзины"""
        cart = self.session.query(ShoppingCart).options(
            joinedload(ShoppingCart.items)
            .joinedload(ShoppingCartItem.product)
        ).get(cart_id)
        
        if not cart:
            return 0.0
        
        sum = 0
        for item in cart.items:
            sum += item.quantity * item.product.price

        return sum