from abc import ABC, abstractmethod

from fastapi import status


class BaseAPIException(ABC, Exception):
    """Base class for all API exceptions"""

    @property
    @abstractmethod
    def default_message(self) -> str:
        pass

    @property
    @abstractmethod
    def example_message(self) -> str:
        pass

    @property
    @abstractmethod
    def http_status_code(self) -> int:
        pass

    @classmethod
    def get_openapi_response(cls) -> dict:
        return {cls.http_status_code: {'description': cls.example_message}}

    def __init__(self, *args) -> None:
        if args:
            super().__init__(self.default_message.format(*args))
        else:
            super().__init__(self.default_message)


class ColumnNotFoundException(BaseAPIException):
    http_status_code = status.HTTP_404_NOT_FOUND
    default_message = 'Column not found in Google sheets document worksheet'
    example_message = default_message


class IncorrectTypeException(BaseAPIException):
    http_status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_message = 'Trying to upload data of incorrect type in a Google sheets column'
    example_message = default_message
