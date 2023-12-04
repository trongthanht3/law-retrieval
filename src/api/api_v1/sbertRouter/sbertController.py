import structlog
import numpy as np
from time import time
from sentence_transformers import SentenceTransformer, util
import pickle
import torch
from config import (
    SBERT_MODEL_PATH,
    CORPUS_EMB
)

logger = structlog.get_logger()

load_time_start = time()
model = SentenceTransformer(SBERT_MODEL_PATH)
model.max_seq_length = 256
load_time_end = time()-load_time_start
logger.info(f"SBERT model loaded in {load_time_end} seconds")
corpus_embedded = pickle.load(open(CORPUS_EMB, 'rb'))

def encode_data(question, answers):
    questionEmb = model.encode(question, convert_to_tensor=True)
    answersEmb = model.encode(answers, convert_to_tensor=True)

    cosine_scores = util.cos_sim(questionEmb, answersEmb)

    return cosine_scores.cpu().numpy()

def compute_score(question):
    questionEmb = model.encode(question, convert_to_tensor=True)
    scores = util.cos_sim(questionEmb.cpu(), corpus_embedded)
    cos_sim = scores.squeeze(0).numpy()
    return cos_sim

