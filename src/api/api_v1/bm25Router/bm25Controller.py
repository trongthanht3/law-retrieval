import structlog
import pandas as pd
import numpy as np
from underthesea import word_tokenize
from utils.utils import pre_process, no_accent_vietnamese
from time import time

import pickle
from config import (
    BM25_MODEL_PATH,
    CORPUS_PATH,
    BM25_ONLY_TEXT_PATH
)

logger = structlog.get_logger()

load_time_start = time()
bm25 = pickle.load(open(BM25_MODEL_PATH, 'rb'))
# ,url,description,law_name,law_id,article_id,article_name,article_content,expDate,isExpire,is_zalo,combine,is_non_url
df_corpus = pd.read_csv(CORPUS_PATH, dtype={"url": str, "description": str, "law_name": str, "law_id": str,
                                            "article_id": int, "article_name": str, "article_content": str,
                                            "expDate": str, "isExpire": str, "is_zalo": bool, "combine": str,
                                            "is_non_url": bool}, index_col=0)
df_corpus_columns = df_corpus.columns
only_text = df_corpus['combine']
pre_search_law_name = df_corpus['law_name'].unique().tolist()
pre_search_law_id = df_corpus['law_id'].unique().tolist()
pre_search_description = df_corpus['description'].unique().tolist()
load_time_end = time() - load_time_start
logger.info(f"BM25 model loaded in {load_time_end} seconds")


# only_text = pickle.load(open(BM25_ONLY_TEXT_PATH, 'rb'))


def pre_search(query):
    if str(query) in pre_search_law_name:
        return df_corpus[df_corpus['law_name'] == query]
    if str(query) in pre_search_law_id:
        return df_corpus[df_corpus['law_id'] == query]
    for description in pre_search_description:
        q = no_accent_vietnamese(str(query).lower())
        d = 'luat ' + no_accent_vietnamese(str(description).lower())
        if q in d and len(d) <= 3*len(q):
            return df_corpus[df_corpus['description'] == description]


def bm25_query(query, top_n=30):
    tokenized_query = word_tokenize(query)
    docs = bm25.get_top_n(tokenized_query, only_text, n=top_n)
    res = [x for x in docs if str(x) != 'nan']
    return res


def get_result_info(docs):
    result = pd.DataFrame(columns=df_corpus_columns)
    for doc in docs:
        result = pd.concat([result, df_corpus[df_corpus['combine'] == doc][:1]], ignore_index=True)
    result.drop(columns=['combine', 'is_zalo', 'is_non_url'], inplace=True)
    return result
