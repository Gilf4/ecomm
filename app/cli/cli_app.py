from .command_dispatcher import CommandDispatcher
from .commands.user_commands import CreateUserCommand, LoginCommand
from .commands.cart_commands import AddToCartCommand
from .commands.create_product import CreateProductCommand
from .strategy.strategies import PaymentContext, CreditCardPayment, SBPPayment, CashPayment
from dao import ShoppingCartDAO


class ECommerceCLI:
    def __init__(self, session):
        self.session = session
        self.dispatcher = CommandDispatcher()
        self.current_user = None
        self.cart_dao = ShoppingCartDAO(session)

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
            print("4. Undo Last Action")
            print("5. View History")
            print("6. Logout")
            
            choice = input("Select option: ")
            
            try:
                if choice == '1':
                    self._add_to_cart_flow()
                elif choice == '2':
                    self._create_product_flow()
                elif choice == '3':
                    self._checkout_flow()
                elif choice == '4':
                    self._undo_last_action()
                elif choice == '5':
                    self._view_history()
                elif choice == '6':
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
            print("Cart is empty or not found.")
            return
        
        total = self.cart_dao.calculate_total(cart.cart_id)
        print(f"\nTotal: ${total:.2f}")
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
        
        if result:
            print("Payment successful!")
        else:
            print("Payment failed")

    def _undo_last_action(self):
        if self.dispatcher.undo():
            print("Last action undone")
        else:
            print("Nothing to undo")

    def _view_history(self):
        print("\nHistory of actions:")
        for i, desc in enumerate(self.dispatcher.get_history(), 1):
            print(f"{i}. {desc}")
