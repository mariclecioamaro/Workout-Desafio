
from pydantic import field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = field(default='postgresql+asyncpg://workout@localhost/workout')

settings = Settings()