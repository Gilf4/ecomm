from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import Base, ProductCategory, User, Product, AttributeValue
from dao import BaseDAO, ProductCategoryDAO, ProductDAO, AttributeDAO, AttributeValueDAO, ShoppingCartItemDAO, ShoppingCartDAO
from config.settings import DATABASE_URL
from dao.user_dao import UserDAO


def init_db():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return engine, session


def init_db():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return engine, session

def create_test_category(session):
    category_dao = ProductCategoryDAO(session)
    return category_dao.create(category_name="Телефон")

def create_test_product(session, category_id):
    product_dao = ProductDAO(session)
    
    # Вариант 1: Создание через kwargs
    return product_dao.create(
        category_id=category_id,
        product_name="Смартфон Samsung",
        product_description="Флагманский смартфон",
        price=89999.99
    )
    
    # ИЛИ Вариант 2: Через экземпляр
    # test_product = Product(
    #     category_id=category_id,
    #     product_name="Смартфон Samsung",
    #     product_description="Флагманский смартфон",
    #     price=89999.99
    # )
    # return product_dao.create(instance=test_product)

def setup_sample_data(session):
    # Инициализация DAO
    product_dao = ProductDAO(session)
    attribute_dao = AttributeDAO(session)
    value_dao = AttributeValueDAO(session)

    # Создаем тестовый продукт
    product = product_dao.create(
        product_name="Смартфон iPhone 15",
        category_id=1,  # Предполагаем, что категория уже создана
        price=99999.99
    )

    # Создаем атрибуты или находим существующие
    color_attr = attribute_dao.find_by_name("Цвет") or \
                 attribute_dao.create(attribute_name="Цвет")
    
    memory_attr = attribute_dao.find_by_name("Память") or \
                  attribute_dao.create(attribute_name="Память")

    # Добавляем значения атрибутов для продукта
    value_dao.create(
        product_id=product.product_id,
        attribute_id=color_attr.attribute_id,
        value="Черный"
    )
    
    value_dao.create(
        product_id=product.product_id,
        attribute_id=memory_attr.attribute_id,
        value="256 ГБ"
    )

    return product

def print_product_attributes(session, product_id):
    value_dao = AttributeValueDAO(session)
    values = value_dao.get_for_product(product_id)
    
    print("\nАтрибуты продукта:")
    for val in values:
        print(f"{val.attribute.attribute_name}: {val.value}")

# if __name__ == "__main__":
#     engine, session = init_db()
    
#     try:
#         cart_dao = ShoppingCartDAO(session)
#         item_dao = ShoppingCartItemDAO(session)

#         cart = cart_dao.get_user_cart(1)
#         cart_dao.add_to_cart(cart.user_id, 4)
#         total = cart_dao.calculate_total(cart.cart_id)


#         if cart:
#             for item in cart.items:
#                 print(f"{item.product.product_name}: {item.quantity} x {item.product.price}")
#             print(f"Total: {total}")
#         else:
#             print("У пользователя пока нет корзины.")
        
#     except Exception as e:
#         print(f"Ошибка: {e}")
#         session.rollback()
#     finally:
#         session.close()
from cli import ECommerceCLI

def main():
    engine, session = init_db()
    
    cli = ECommerceCLI(session)
    cli.start()

if __name__ == "__main__":
    main()



