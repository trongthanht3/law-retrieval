from peewee import *
from config import (
    DATABASE_HOSTNAME,
    _DATABASE_CREDENTIAL_USER,
    _DATABASE_CREDENTIAL_PASSWORD,
    DATABASE_NAME,
    DATABASE_HOST,
    DATABASE_PORT,
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# pgs_qldb = PostgresqlDatabase(DATABASE_HOSTNAME, user=_DATABASE_CREDENTIAL_USER,
#                         password=_DATABASE_CREDENTIAL_PASSWORD, database=DATABASE_NAME,
#                         host=DATABASE_HOST, port=DATABASE_PORT)

engine = create_engine("postgresql+psycopg2://postgres:123456@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()

