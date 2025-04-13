from sqlalchemy.orm import Session
from models import ShoppingCartItem
from .base_dao import BaseDAO

class ShoppingCartItemDAO(BaseDAO):
    def __init__(self, session: Session):
        super().__init__(session, ShoppingCartItem)

    def find_item(self, cart_id, product_id) -> ShoppingCartItem | None:
        """Поиск конкретного товара в корзине"""
        return self.session.query(ShoppingCartItem).filter(
            ShoppingCartItem.cart_id == cart_id,
            ShoppingCartItem.product_id == product_id
        ).first()
    
    def add_item(self, cart_id, product_id, quantity = 1) -> ShoppingCartItem:
        """Добавление нового товара в корзину (quantity=1)"""
        return self.create(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity
        )
    
    def increase_quantity(self, item_id, amount = 1) -> ShoppingCartItem | None:
        """Увеличение количества товара"""
        item = self.get_by_id(item_id)
        if item:
            self.update(item_id, quantity=item.quantity + amount)
        return item