from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Boolean, INTEGER
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from .query import Query

class Base(DeclarativeBase):
    pass


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id: Mapped[int] = mapped_column(primary_key=True)
    law_id: Mapped[str] = mapped_column(String())
    article_id: Mapped[int] = mapped_column(INTEGER())
    user_label: Mapped[bool] = mapped_column(Boolean())
    query_id: Mapped[int] = mapped_column(INTEGER(), ForeignKey(Query.id))

    def __repr__(self) -> str:
        return f"UserFeedback(id={self.id!r}, law_id={self.law_id!r}, article_id={self.article_id!r}, user_label={self.user_label!r}, query_id={self.query_id!r})"
