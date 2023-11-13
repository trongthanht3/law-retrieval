import uvicorn

import structlog
import asyncio
from fastapi import FastAPI, Request

from api.api_v1.api import api_router
from customLogging import configure_logger

import config

# setup logging
customLogger = structlog.stdlib.get_logger()
configure_logger()


app = FastAPI(
    title="Python Backend API",
    # root_path="/api/v1",
    docs_url="/swagger",
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)
app.logger = customLogger

app.include_router(api_router, prefix="/api/v1")


@app.get("/ping")
async def ping():
    await log.info(config.DATABASE_HOSTNAME)
    return {"ping": "pong!"}

async def main():
    config = uvicorn.Config(
        app,
        port=5000,
        host="0.0.0.0",
        log_level="info",
        reload=True,
        reload_dirs=["*"],
        # reload_includes=["src"],
        # root_path="../"
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    # asyncio.run(main())
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=5000,
        log_level="info",
        reload=True,
        reload_dirs=["."],
    )


