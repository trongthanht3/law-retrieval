import pandas as pd
import numpy as np
import json
import torch

from api.api_v1.sbertRouter import sbertController
from api.api_v1.bm25Router import bm25Controller
from utils.utils import pre_process

from config import (
    RANGE_SCORE
)


def law_retrieval(query, top_n):
    pre_search = bm25Controller.pre_search(query)
    if pre_search is not None:
        pre_search['score'] = 1
        return json.loads(pre_search.to_json(orient='records'))
    # bm25res = bm25Controller.bm25_query(query, top_n)
    bm25scores = bm25Controller.bm25_query_with_score(query)
    cosim_scores = sbertController.compute_score([query])

    new_scores = bm25scores * cosim_scores
    max_score = np.max(new_scores)
    new_scores = torch.tensor(new_scores)
    final_scores, indices = torch.topk(new_scores, top_n)
    map_ids = [int(idx) for score, idx in zip(final_scores, indices) if
               float(score) >= max_score - float(RANGE_SCORE) and float(score) <= max_score]
    combine_scores = [float(score) for score, idx in zip(final_scores, indices) if
               float(score) >= max_score - float(RANGE_SCORE) and float(score) <= max_score]
    # print("bm25:", torch.topk(torch.tensor(bm25scores), top_n))
    # print("combine:", combine_scores)
    bm25res_full_info = bm25Controller.get_result_info_by_ids(map_ids)
    bm25res_full_info['score'] = combine_scores

    # bm25res_full_info = bm25Controller.get_result_info(bm25res)
    #
    # print(len(bm25res_full_info), len(cosin_scores[0]))
    # bm25res_full_info['score'] = cosin_scores[0]
    # bm25res_full_info = bm25res_full_info.sort_values("score", ascending=False)

    return json.loads(bm25res_full_info.to_json(orient='records'))
