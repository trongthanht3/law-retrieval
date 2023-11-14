import pandas as pd
import numpy as np
import json

from api.api_v1.sbertRouter import sbertController
from api.api_v1.bm25Router import bm25Controller
from utils.utils import pre_process

from config import (
    CORPUS_PATH
)

def law_retrieval(query, top_n):
    pre_search = bm25Controller.pre_search(query)
    if pre_search is not None:
        pre_search['score'] = 1
        return json.loads(pre_search.to_json(orient='records'))
    bm25res = bm25Controller.bm25_query(query, top_n)
    bm25res_full_info = bm25Controller.get_result_info(bm25res)

    cosin_scores = sbertController.encode_data([query], bm25res)
    print(len(bm25res_full_info), len(cosin_scores[0]))
    bm25res_full_info['score'] = cosin_scores[0]
    bm25res_full_info = bm25res_full_info.sort_values("score", ascending=False)

    return json.loads(bm25res_full_info.to_json(orient='records'))
