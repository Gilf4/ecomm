from .command_dispatcher import CommandDispatcher
from .commands.user_commands import CreateUserCommand, LoginCommand
from .commands.cart_commands import AddToCartCommand
from .commands.create_product import CreateProductCommand
from .strategy.strategies import PaymentContext, CreditCardPayment, SBPPayment, CashPayment
from .statePattern.states import Order
from dao import ShoppingCartDAO


class ECommerceCLI:
    def __init__(self, session):
        self.session = session
        self.dispatcher = CommandDispatcher()
        self.current_user = None
        self.cart_dao = ShoppingCartDAO(session)
        self.orders = [] 

    def start(self):
        self._welcome_screen()
        if self.current_user:
            self._main_menu()

    def _welcome_screen(self):
        while True:
            print("\nWelcome to E-Commerce CLI")
            print("1. Create User")
            print("2. Login")
            print("3. Exit")
            choice = input("Choose an option: ")

            try:
                if choice == '1':
                    self._create_user_flow()
                elif choice == '2':
                    self._login_flow()
                    if self.current_user:
                        print(f"Logged in as {self.current_user.email}")
                        return
                elif choice == '3':
                    exit()
                else:
                    print("Invalid choice")
            except Exception as e:
                print(f"Error: {str(e)}")

    def _main_menu(self):
        while True:
            print(f"\nMain Menu — Logged in as {self.current_user.email}")
            print("1. Add item to Cart")
            print("2. Create Product")
            print("3. Checkout")
            print("4. Track Order")
            print("5. Undo Last Action")
            print("6. View History")
            print("7. Logout")
            
            choice = input("Select option: ")
            
            try:
                if choice == '1':
                    self._add_to_cart_flow()
                elif choice == '2':
                    self._create_product_flow()
                elif choice == '3':
                    self._checkout_flow()
                elif choice == '4':
                    self._track_order_flow()
                elif choice == '5':
                    self._undo_last_action()
                elif choice == '6':
                    self._view_history()
                elif choice == '7':
                    self.current_user = None
                    print("Logged out.")
                    self._welcome_screen()
                    break
                else:
                    print("Invalid choice")
            except Exception as e:
                print(f"Error: {str(e)}")

    def _create_user_flow(self):
        user_data = {
            'email': input("Email: "),
            'password_hash': input("Password: "),
            'first_name': input("First Name: "),
            'last_name': input("Last Name: "),
        }
        command = CreateUserCommand(self.session, user_data)
        self.current_user = command.execute()
        print("User created and logged in successfully")

    def _login_flow(self):
        email = input("Email: ")
        password = input("Password: ")
        command = LoginCommand(self.session, email, password)
        user = command.execute()
        if user:
            self.current_user = user
        else:
            print("Login failed")

    def _add_to_cart_flow(self):
        product_id = int(input("Product ID: "))
        command = AddToCartCommand(self.session, self.current_user.user_id, product_id)
        result = self.dispatcher.execute(command)
        if result:
            print("Item added to cart")
        else:
            print("Failed to add item")

    def _create_product_flow(self):
        command = CreateProductCommand(self.session)
        product = self.dispatcher.execute(command)
        if product:
            print(f"Product created! ID: {product.product_id}")
            print("Attributes:")
            for attr in product.attribute_values:
                print(f"  {attr.attribute.attribute_name}: {attr.value}")

    def _checkout_flow(self):
        cart = self.cart_dao.get_user_cart(self.current_user.user_id)
        if not cart:
            print("Ваша корзина пуста!")
            return
        
        print("\nВаш заказ:")
        for item in cart.items:
            print(f"{item.product.product_name} x{item.quantity} - ${item.product.price * item.quantity:.2f}")
        
        total = self.cart_dao.calculate_total(cart.cart_id)
        print(f"\nИтого к оплате: ${total}")

        print("Select payment method:")
        print("1. Credit Card")
        print("2. SBP")
        print("3. Cash")
        choice = input("Your choice: ")
        
        context = PaymentContext()
        result = False
        
        if choice == '1':
            context.set_strategy(CreditCardPayment())
            card_data = {
                'card_number': input("Card number: "),
                'expiry_date': input("Expiry (MM/YY): "),
                'cvv': input("CVV: ")
            }
            result = context.execute_payment(total, **card_data)
        elif choice == '2':
            context.set_strategy(SBPPayment())
            result = context.execute_payment(total, phone=input("Your phone: "))
        elif choice == '3':
            context.set_strategy(CashPayment())
            result = context.execute_payment(total)
        else:
            print("Invalid choice")
            return
        
        payment_successful = False

        if result:
            print("Payment successful!")
            payment_successful = True
        else:
            print("Payment failed")
        
        if payment_successful:
            order_id = len(self.orders) + 1
            new_order = Order(order_id, total)
            self.orders.append(new_order)

            for item in cart.items:
                self.session.delete(item)
            self.session.commit()
            
            print(f"\nОплата прошла успешно! Номер вашего заказа: #{order_id}")

    def _track_order_flow(self):
        if not self.orders:
            print("У вас нет активных заказов")
            return
        
        print("\nВаши заказы:")
        for order in self.orders:
            print(f"#{order.order_id} - {order.get_status()} - ${order.total}")
        
        order_id = input("Введите номер заказа для отслеживания: ")
        try:
            order_id = int(order_id)
            order = next((o for o in self.orders if o.order_id == order_id), None)

            if not order:
                print(f"Заказ #{order_id} не найден. Проверьте номер заказа.")
            
            if order:
                order.track(interval=3)
            else:
                print("Заказ не найден")
        except ValueError:
            print("Некорректный номер заказа")

    def _undo_last_action(self):
        if self.dispatcher.undo():
            print("Last action undone")
        else:
            print("Nothing to undo")

    def _view_history(self):
        print("\nHistory of actions:")
        for i, desc in enumerate(self.dispatcher.get_history(), 1):
            print(f"{i}. {desc}")
