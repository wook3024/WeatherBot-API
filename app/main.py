import asyncio
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_408_REQUEST_TIMEOUT

from . import cfg, logger
from .routes import index, weather


def create_app() -> FastAPI:
    app = FastAPI(
        title=cfg.service.app.title,
        version=cfg.service.app.version,
        default_response_class=ORJSONResponse,
    )

    app.include_router(router=index.router, tags=["Index"])
    app.include_router(router=weather.router, tags=["Weather"])

    return app


app = create_app()


@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        start_time = time.time()
        return await asyncio.wait_for(
            call_next(request), timeout=cfg.service.app.timeout
        )
    except asyncio.TimeoutError:
        return ORJSONResponse(
            status_code=HTTP_408_REQUEST_TIMEOUT,
            content=jsonable_encoder(
                {"detail": "Request processing time excedeed limit"}
            ),
        )
    finally:
        process_time = time.time() - start_time
        logger.info(
            "{0} process time: {1:.8f}s".format(call_next.__name__, process_time)
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return ORJSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=cfg.service.app.host,
        port=cfg.service.app.port,
        reload=cfg.service.app.reload,
        log_level=cfg.log.log_level,
    )
