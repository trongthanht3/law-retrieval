import structlog
import numpy as np
from time import time
from sentence_transformers import SentenceTransformer, util

logger = structlog.get_logger()

load_time_start = time()
model = SentenceTransformer("vinai/phobert-base-v2")
model.max_seq_length = 256
load_time_end = time()-load_time_start
logger.info(f"SBERT model loaded in {load_time_end} seconds")

def encode_data(question, answers):
    questionEmb = model.encode(question, convert_to_tensor=True)
    answersEmb = model.encode(answers, convert_to_tensor=True)

    cosine_scores = util.cos_sim(questionEmb, answersEmb)

    return cosine_scores
