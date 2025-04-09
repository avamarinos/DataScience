import os
from pydantic import BaseSettings
# configuration settings for the application
class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL","postgresql://user:password@db/uber")

settings = Settings()