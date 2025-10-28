import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()