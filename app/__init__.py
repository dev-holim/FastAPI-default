from typing import Union, Callable, AsyncContextManager
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.types import Lifespan

from app.api import include_routers
from app.adapter.repository.rdb import init_rdb
from app.adapter.repository.cache import init_cache
from app.security.cors import include_cors_middleware

@asynccontextmanager
async def lifespan_(app: FastAPI):
    await init_rdb()
    await init_cache()

    yield


def create_app(
        lifespan: Union[
            Lifespan,
            AsyncContextManager[
                Callable[[FastAPI], ...]
            ]
        ]
):
    from app.const import openapi_tags

    app = FastAPI(
        lifespan=lifespan,
        openapi_tags=openapi_tags,
        swagger_ui_parameters={"operationsSorter": "method"},
    )
    include_routers(app)
    include_cors_middleware(app)

    return app
