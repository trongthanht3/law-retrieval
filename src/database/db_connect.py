from peewee import *
from src.config import (
    DATABASE_HOSTNAME,
    _DATABASE_CREDENTIAL_USER,
    _DATABASE_CREDENTIAL_PASSWORD,
    DATABASE_NAME,
    DATABASE_HOST,
    DATABASE_PORT,
)

pgs_qldb = PostgresqlDatabase(DATABASE_HOSTNAME, user=_DATABASE_CREDENTIAL_USER,
                        password=_DATABASE_CREDENTIAL_PASSWORD, database=DATABASE_NAME,
                        host=DATABASE_HOST, port=DATABASE_PORT)

