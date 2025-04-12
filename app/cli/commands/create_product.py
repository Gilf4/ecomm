from ..builders.product_builder import ProductBuilder
from ..command import Command

class CreateProductCommand(Command):
    def __init__(self, session):
        self.session = session
        self.created_product = None

    def execute(self):
        try:
            builder = ProductBuilder(self.session)
            
            builder.with_name(input("Product name: ")).with_price(float(input("Price: "))).with_category(input("Category: "))

            if input("Add description? (y/n): ").lower() == 'y':
                builder.with_description(input("Description: "))

            while True:
                if input("Add attribute? (y/n): ").lower() != 'y':
                    break
                name = input("Attribute name: ")
                value = input("Attribute value: ")
                builder.with_attribute(name, value)

            self.created_product = builder.build()
            return self.created_product
        
        except Exception as e:
            self.session.rollback()
            print(f"Error creating product: {str(e)}")
            return None

    def undo(self):
        if self.created_product:
            self.session.delete(self.created_product)
            self.session.commit()

    def description(self):
        if self.created_product:
            return f"Created product {self.created_product.product_name} (ID: {self.created_product.product_id})"
        return "Product creation (failed)"