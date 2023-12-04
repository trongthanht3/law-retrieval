from pydantic import BaseModel, Required

class QueryInput(BaseModel):
    query: str
    top_n: int = 30

class FeedbackInput(BaseModel):
    query_id: int
    law_id: str
    article_id: int
    user_label: bool
