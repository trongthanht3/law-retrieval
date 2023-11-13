# import pika
# import logging
# import json
# import uuid
# import asyncio
# from starlette.config import Config
# from aio_pika import connect_robust
#
#
# from .logging import setup_logging
#
# config = Config(".env")
#
# # configure logging
# log = logging.getLogger(__name__)
# setup_logging()
#
#
# class PikaClient:
#     def __init__(self, process_callable):
#         self.publish_queue_name = config("RABBIT_PUBLISH_QUEUE_NAME", default="publish_queue")
#         self.connection = pika.BlockingConnection(
#             pika.ConnectionParameters(host=config("RABBIT_HOST", default="localhost"))
#         )
#         self.channel = self.connection.channel()
#         self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
#         self.callback_queue = self.publish_queue.method.queue
#         self.response = None
#         self.process_callable = process_callable
#         log.info('Pika connection initialized')
#
#     async def consume(self, loop):
#         """Setup message listener with the current running loop"""
#         connection = await connect_robust(host=config("RABBIT_HOST", default="localhost"),
#                                           port=config("RABBIT_PORT", default="5672"),
#                                           loop=loop)
#         channel = await connection.channel()
#         queue = await channel.declare_queue(config("RABBIT_CONSUME_QUEUE_NAME", default="consume_queue"))
#         await queue.consume(self.process_incoming_message, no_ack=False)
#         log.info('Established pika async listener')
#         return connection
#
#     async def process_incoming_message(self, message):
#         """Processing incoming message from RabbitMQ"""
#         message.ack()
#         body = message.body
#         if body:
#             self.process_callable(json.loads(body.strip()))
#
#     async def send_message(self, message: dict):
#         """Method to publish message to RabbitMQ"""
#         # log.info("PUBLISH_QUEUE_NAME: ", self.publish_queue_name)
#         print("I GOT MESSAGE: ", message)
#         print("[+] SENDING MESSAGE")
#         self.channel.basic_publish(
#             exchange='',
#             routing_key=self.publish_queue_name,
#             properties=pika.BasicProperties(
#                 reply_to=self.callback_queue,
#                 correlation_id=str(uuid.uuid4())
#             ),
#             body=json.dumps(message, ensure_ascii=False)
#         )