import structlog
from fastapi import FastAPI, Request, APIRouter
import psycopg2
from schemas.schemas import QueryInput, FeedbackInput
from database.db_connect import session
from database.models.query import Query

import api.api_v1.lawRetrievalRouter.lawRetrievalController as lawRetrievalController

router = APIRouter()
logger = structlog.get_logger()


@router.post("/lawRetrieval", status_code=200)
async def _law_retrieval(payload: QueryInput, request: Request):
    res = []
    try:
        query = payload.query
        top_n = payload.top_n
        res, res_law_id = lawRetrievalController.law_retrieval(query, top_n)
        user_query = Query(query=query, relevant_documents=str(res_law_id))
        session.add(user_query)
        session.commit()
        session.flush()
        session.refresh(user_query)
        logger.info("Query: ", user_query.id)
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
