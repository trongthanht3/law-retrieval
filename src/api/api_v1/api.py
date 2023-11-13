from fastapi import APIRouter

# from .endpoints import chat
from .bm25Router import bm25Service
from .sbertRouter import sbertService
from .lawRetrievalRouter import lawRetrievalService

api_router = APIRouter()

# api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(bm25Service.router, prefix="/bm25Router", tags=["bm25Router"])
api_router.include_router(sbertService.router, prefix="/sbertRouter", tags=["sbertRouter"])
api_router.include_router(lawRetrievalService.router, prefix="/lawRetrievalRouter", tags=["lawRetrievalRouter"])
