import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from . import cfg, logger
from .routes import index, weather


def create_app() -> FastAPI:
    app = FastAPI(
        title=cfg.service.app.title,
        version=cfg.service.app.version,
        default_response_class=ORJSONResponse,
    )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            "{0} process time: {1:.8f}s".format(call_next.__name__, process_time)
        )
        return response

    app.include_router(router=index.router, tags=["Index"])
    app.include_router(router=weather.router, tags=["Weather"])

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=cfg.service.app.host,
        port=cfg.service.app.port,
        reload=cfg.service.app.reload,
        log_level=cfg.log.log_level,
    )
