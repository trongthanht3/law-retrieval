import logging
import os
from urllib import parse
from starlette.datastructures import Secret
from starlette.config import Config

log = logging.getLogger(__name__)

print("WHERE AM I:", os.getcwd())

config = Config(".env")

# configure logging

# logging
LOG_LEVEL = config("LOG_LEVEL", default="info")

# database
DATABASE_HOSTNAME = config("DATABASE_HOSTNAME")
DATABASE_CREDENTIALS = config("DATABASE_CREDENTIALS", cast=Secret)
# this will support special chars for credentials
_DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(DATABASE_CREDENTIALS).split(":")
_QUOTED_DATABASE_PASSWORD = parse.quote(str(_DATABASE_CREDENTIAL_PASSWORD))
DATABASE_NAME = config("DATABASE_NAME", default="dispatch")
DATABASE_HOST = config("DATABASE_HOST", default="localhost")
DATABASE_PORT = config("DATABASE_PORT", default="5432")
