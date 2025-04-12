from .command_dispatcher import CommandDispatcher
from .commands.user_commands import CreateUserCommand
from .commands.cart_commands import AddToCartCommand
from .commands.create_product import CreateProductCommand


class ECommerceCLI:
    def __init__(self, session):
        self.session = session
        self.dispatcher = CommandDispatcher()
        self.current_user = None

    def start(self):
        while True:
            print("\nE-Commerce CLI")
            print("1. Create User")
            print("2. Add item to Cart")
            print("3. Create Product")
            print("4. Undo Last Action")
            print("5. View History")
            print("6. Exit")
            
            choice = input("Select option: ")
            
            try:
                if choice == '1':
                    self._create_user_flow()
                elif choice == '2':
                    self._add_to_cart_flow()
                elif choice == '3':
                    self._create_product_flow()
                elif choice == '4':
                    self._undo_last_action()
                elif choice == '5':
                    self._view_history()
                elif choice == '6':
                    break
                else:
                    print("Invalid choice")
            except Exception as e:
                print(f"Error: {str(e)}")

    def _create_product_flow(self):
        command = CreateProductCommand(self.session)
        product = self.dispatcher.execute(command)
        if product:
            print(f"Product created! ID: {product.product_id}")
            print("Attributes:")
            for attr in product.attribute_values:
                print(f"  {attr.attribute.attribute_name}: {attr.value}")
        
    def _create_user_flow(self):
        user_data = {
            'email': input("Email: "),
            'password_hash': input("Password: "),
            'first_name': input("First Name: "),
            'last_name': input("Last Name: "),
        }
        command = CreateUserCommand(self.session, user_data)
        self.dispatcher.execute(command)
        print("User created successfully")

    def _add_to_cart_flow(self):
        user_id = int(input("User ID: "))
        product_id = int(input("Product ID: "))
        command = AddToCartCommand(self.session, user_id, product_id)
        result = self.dispatcher.execute(command)
        if result:
            print("Item added to cart")
        else:
            print("Failed to add item")

    def _undo_last_action(self):
        if self.dispatcher.undo():
            print("Last action undone")
        else:
            print("Nothing to undo")

    def _view_history(self):
        print("\nHistory of action:")
        for i, desc in enumerate(self.dispatcher.get_history(), 1):
            print(f"{i}. {desc}")