from .config import load_db_config

db_config = load_db_config()

DATABASE_URL = db_config.url 