from enum import Enum

from pydantic_settings import BaseSettings


class Environment(str, Enum):
    PROD = 'PROD'
    TEST = 'TEST'
    DEV = 'DEV'


class Settings(BaseSettings):
    ENVIRONMENT: Environment = Environment.DEV
    REMOTE_BROWSER: bool = False

    WEB_APP_TITLE: str = 'Whatsapp Web Selenium Python API'
    WEB_APP_DESCRIPTION: str = 'Api to automatize whatsapp web operations like send limited bulk messages'
    WEB_APP_VERSION: str = '1.0.0'

    OPENAPI_SERVER: str = ''

    class Config:
        env_file = 'dev.env', 'test.dev', 'prod.env'
        env_file_encoding = 'utf-8'


settings = Settings()
