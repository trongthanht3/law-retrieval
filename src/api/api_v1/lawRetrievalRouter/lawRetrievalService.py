import structlog
from fastapi import FastAPI, Request, APIRouter

from schemas.schemas import QueryInput

import api.api_v1.lawRetrievalRouter.lawRetrievalController as lawRetrievalController

router = APIRouter()
logger = structlog.get_logger()


@router.post("/lawRetrieval", status_code=200)
async def _law_retrieval(payload: QueryInput, request: Request):
    res = []
    try:
        query = payload.query
        top_n = payload.top_n
        res = lawRetrievalController.law_retrieval(query, top_n)
    except Exception as e:
        await logger.error(e)
        res = e

    return {res: res}
