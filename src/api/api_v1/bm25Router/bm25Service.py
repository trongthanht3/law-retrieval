import structlog
from fastapi import FastAPI, Request, APIRouter

from schemas.schemas import QueryInput

import api.api_v1.bm25Router.bm25Controller as bm25Controller

router = APIRouter()
logger = structlog.get_logger()


@router.post("/bm25query")
async def _bm25_query(payload: QueryInput, request: Request):
    res = []
    try:
        query = payload.query
        top_n = payload.top_n
        await logger.debug("Query: ", query)
        res = bm25Controller.bm25_query(query, top_n)
    except Exception as e:
        await logger.error(e)
        res = e
    return {"res": res}
