from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    db_name: SecretStr
    db_user: SecretStr
    db_pass: SecretStr
    db_port: SecretStr
    db_host: SecretStr
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
