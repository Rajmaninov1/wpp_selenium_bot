from enum import Enum

from pydantic_settings import BaseSettings


class Environment(str, Enum):
    PROD = 'PROD'
    TEST = 'TEST'
    DEV = 'DEV'


class Settings(BaseSettings):

    REMOTE_BROWSER: bool = False

    class Config:
        env_file = 'dev.env', 'test.dev', 'prod.env'
        env_file_encoding = 'utf-8'


settings = Settings()
