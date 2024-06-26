import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv, load_dotenv

# DOTENV = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(case_sensitive=False)


settings = Settings()