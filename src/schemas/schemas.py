from pydantic import BaseModel

class QueryInput(BaseModel):
    query: str
    top_n: int = 30

