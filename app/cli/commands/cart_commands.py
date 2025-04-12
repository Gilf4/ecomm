from ..command import Command
from dao import ShoppingCartDAO
from dao import ShoppingCartItemDAO

class AddToCartCommand(Command):
    def __init__(self, session, user_id: int, product_id: int):
        self.session = session
        self.user_id = user_id
        self.product_id = product_id
        self.cart_dao = ShoppingCartDAO(session)
        self.item_dao = ShoppingCartItemDAO(session)
        self.added_item = None
        self.prev_quantity = 0

    def execute(self):
        cart = self.cart_dao.get_user_cart(self.user_id)
        if not cart:
            cart = self.cart_dao.create(user_id=self.user_id)
        
        existing_item = self.item_dao.find_item(cart.cart_id, self.product_id)
        if existing_item:
            self.prev_quantity = existing_item.quantity
            self.item_dao.update(
                existing_item.item_id, 
                quantity=self.prev_quantity + 1
            )
            self.added_item = existing_item
        else:
            self.added_item = self.item_dao.add_item(
                cart.cart_id, 
                self.product_id
            )
        return self.added_item

    def undo(self) -> None:
        if not self.added_item:
            return
        
        cart = self.cart_dao.get_by_id(self.added_item.cart_id)
        if cart and len(cart.items) == 1:
            self.cart_dao.delete(cart.cart_id)
        else:
            if self.prev_quantity > 0:
                self.item_dao.update(
                    self.added_item.item_id,
                    quantity=self.prev_quantity
                )
            else:
                self.item_dao.delete(self.added_item.item_id)
    
    def description(self):
        return f"Added product {self.product_id} to cart"