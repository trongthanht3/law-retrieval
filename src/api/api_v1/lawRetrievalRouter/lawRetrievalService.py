import structlog
from fastapi import FastAPI, Request, APIRouter
import psycopg2
from schemas.schemas import QueryInput, FeedbackInput
from database.db_connect import session


import api.api_v1.lawRetrievalRouter.lawRetrievalController as lawRetrievalController

router = APIRouter()
logger = structlog.get_logger()


@router.post("/lawRetrieval", status_code=200)
async def _law_retrieval(payload: QueryInput, request: Request):
    res = []
    try:
        query = payload.query
        top_n = payload.top_n
        user_query, res = lawRetrievalController.law_retrieval(query, top_n)
        return {
            "id": user_query.id,
            "data": res
        }
    except Exception as e:
        await logger.error(e)
        res = e
        return res



@router.post("/userFeedback", status_code=200)
async def _user_feedback(payload: FeedbackInput, request: Request):
    res = []
    try:
        feedback_id = lawRetrievalController.user_feedback(payload.query_id,
                                             payload.law_id,
                                             payload.article_id,
                                             payload.user_label)
        return {
            "id": feedback_id,
        }
    except Exception as e:
        await logger.error(e)
        res = e
        return res
