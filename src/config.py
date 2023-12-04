import os
from urllib import parse
from starlette.datastructures import Secret
from starlette.config import Config


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
CORPUS_PATH = config("CORPUS_PATH", default="src/database/law_corpus.csv")

# ML model
BM25_MODEL_PATH = config("BM25_MODEL_PATH", default="bm25_model")
BM25_ONLY_TEXT_PATH = config("BM25_ONLY_TEXT_PATH", default="bm25_model")
SBERT_MODEL_PATH = config("SBERT_MODEL_PATH", default="src/models/sbertv2")
CORPUS_EMB = config("CORPUS_EMB", default="src/model/corpus_emb.sav")
RANGE_SCORE = config("RANGE_SCORE", default=2.6)
