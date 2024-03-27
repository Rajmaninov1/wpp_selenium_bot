from typing import Optional

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.requests import Request


class HTTPBasicOptional(HTTPBasic):
    async def __call__(self, request: Request) -> Optional[HTTPBasicCredentials]:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            return None

        return await super().__call__(request)
