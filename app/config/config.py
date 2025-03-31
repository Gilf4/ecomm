import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class DatabaseConfig:
    user: str
    password: str
    host: str
    port: str
    name: str

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

def load_db_config() -> DatabaseConfig:
    """Загружает конфигурацию БД из .env файла или переменных окружения"""
    load_dotenv()
    
    return DatabaseConfig(
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        name=os.getenv("DB_NAME", "test_db")
    )