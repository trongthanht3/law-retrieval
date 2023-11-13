import pandas as pd
import numpy as np

from api.api_v1.sbertRouter import sbertController
from api.api_v1.bm25Router import bm25Controller
from utils.utils import pre_process

from config import (
    CORPUS_PATH
)

def law_retrieval(query, top_n):
    bm25res = bm25Controller.bm25_query(query, top_n)
    bm25res_full_info = bm25Controller.get_result_info(bm25res)

    cosin_scores = sbertController.encode_data([query], bm25res)

    return cosin_scores
