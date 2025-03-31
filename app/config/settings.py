from .config import load_db_config

# Загружаем конфигурацию базы данных
db_config = load_db_config()

# URL для подключения к базе данных
DATABASE_URL = db_config.url 