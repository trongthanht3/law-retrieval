import structlog
from fastapi import FastAPI, Request, APIRouter

from schemas.schemas import QueryInput

import api.api_v1.sbertRouter.sbertController as sbertController

router = APIRouter()

# @router.post("/sbertRanking")
# async def _bm25query(payload: MessageSchema, request: Request):
#     query = payload.message
#     res = bm25Controller.bm25query(query)
#
#     return {"res": res}
