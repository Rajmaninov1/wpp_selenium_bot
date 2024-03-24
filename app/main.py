import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.exceptions import ExceptionMiddleware

from config.logger_factory import logger_factory
from config.settings import settings, Environment
from middleware.middlewares import add_error_handlers
from routers.routers import add_routers

logger = logging.getLogger('_api_')

# Configure logging
logger_factory()

# Configure FastAPI
if settings.ENVIRONMENT != Environment.PROD:
    settings.WEB_APP_DESCRIPTION = f'## ENV: {settings.ENVIRONMENT}\n\n{settings.WEB_APP_DESCRIPTION}'


@asynccontextmanager
async def lifespan(lifespan_app: FastAPI):
    # Force to build middleware stack for all apps and fill the
    # "middleware_stack" property
    client = TestClient(app)
    # Main app
    client.get('/docs?__lifespan__start__')
    # Sub apps
    # client.get('/admin/docs?__lifespan__start__')

    for current_app in [app]:
        if not current_app:
            continue
        # Hack ExceptionMiddleware to handle (500 or Exception) errors
        # Override on startup because is the moment when the middleware_stack was built
        # Breaking change, only works from 0.91.0 to upper: https://fastapi.tiangolo.com/release-notes/#0910
        generic_exception_handlers = {
            k: v for k, v in current_app.exception_handlers.items() if k == 500 or k == Exception}  # noqa
        if generic_exception_handlers:
            _app = current_app.middleware_stack
            while True:
                if isinstance(_app, ExceptionMiddleware):
                    _app._exception_handlers.update(generic_exception_handlers)  # noqa
                    break
                elif hasattr(_app, 'app'):
                    _app = _app.app
                else:
                    break
    yield

app = FastAPI(
    title=settings.WEB_APP_TITLE,
    description=settings.WEB_APP_DESCRIPTION,
    version=settings.WEB_APP_VERSION,
    servers=[
        {'url': settings.OPENAPI_SERVER, 'description': f'{settings.ENVIRONMENT} environment'},
    ] if settings.OPENAPI_SERVER else None,
    lifespan=lifespan
)

# Configure HTTP Starlette server
add_error_handlers(app)

# Configure routes
add_routers(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
