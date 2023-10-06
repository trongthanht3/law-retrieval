import logging
from src.rabbitmq_client import PikaClient
from fastapi import FastAPI, Request, APIRouter

from src.schemas.schemas import MessageSchema

log = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ping_rabbit")
async def ping_rabbit(payload: MessageSchema, request: Request):
    await request.app.pika_client.send_message(
        {"message": payload.message}
    )
    print("TRUE MESSAGE: ", payload.message)
    # print("CONSUME: ", request.app.pika_client.consume())

    return {"status": "ok"}