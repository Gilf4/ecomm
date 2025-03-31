from sqlalchemy import create_engine, inspect
from models import Base
from config.settings import DATABASE_URL

def init_db():
    engine = create_engine(DATABASE_URL)
    
    Base.metadata.create_all(engine)
    
    return engine

if __name__ == "__main__":
    engine = init_db()
    print("База данных успешно инициализирована!")


