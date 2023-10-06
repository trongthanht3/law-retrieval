import logging
import asyncio
from fastapi import FastAPI, Request


from .api.api_v1.api import api_router
from src.schemas.schemas import MessageSchema
from .logging import setup_logging
from .rabbitmq_client import PikaClient

# setup logging
log = logging.getLogger(__name__)
setup_logging()

class FastAPIRabbit(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message)

    @classmethod
    def log_incoming_message(cls, message: dict):
        """Method to do something meaningful with the incoming message"""
        log.info('Here we got incoming message %s', message)

app = FastAPIRabbit(
    title="LLM Backend API",
    # root_path="/api/v1",
    docs_url="/swagger",
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    log.info("Starting up...")
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task


@app.get("/ping")
async def ping():
    return {"ping": "pong!"}


# async def main():
#     config = uvicorn.Config(
#         app,
#         port=5000,
#         host="0.0.0.0",
#         log_level="info",
#         reload=True
#     )
#     server = uvicorn.Server(config)
#     await server.serve()
#
# if __name__ == "__main__":
#     asyncio.run(main())

