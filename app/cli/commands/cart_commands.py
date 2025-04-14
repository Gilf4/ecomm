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
        self.was_new_cart = False
        self.was_new_item = False

    def execute(self):
        try:
            cart = self.cart_dao.get_user_cart(self.user_id)
            
            if not cart:
                cart = self.cart_dao.create(user_id=self.user_id)
                self.was_new_cart = True
            
            existing_item = self.item_dao.find_item(cart.cart_id, self.product_id)
            
            if existing_item:
                self.prev_quantity = existing_item.quantity
                existing_item.quantity += 1
                self.added_item = existing_item
            else:
                self.added_item = self.item_dao.add_item(
                    cart.cart_id, 
                    self.product_id
                )
                self.was_new_item = True
            
            self.session.commit()

            return self.added_item
            
        except Exception as e:
            self.session.rollback()
            raise

    def undo(self) -> None:
        if not self.added_item:
            return
            
        try:
            # Если это была полностью новая корзина - удаляем её
            if self.was_new_cart:
                self.cart_dao.delete(self.added_item.cart_id)
                return
                
            # Если это был новый элемент - удаляем его
            if self.was_new_item:
                self.item_dao.delete(self.added_item.item_id)
            else:
                # Иначе возвращаем предыдущее количество
                self.item_dao.update(
                    self.added_item.item_id,
                    quantity=self.prev_quantity
                )
                
                self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Undo failed: {str(e)}")

    def description(self):
        return f"Added product {self.product_id} to user {self.user_id} cart"