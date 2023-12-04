from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Query(Base):
    __tablename__ = "law_corpus"

    id: Mapped[int] = mapped_column(primary_key=True)
    query: Mapped[str] = mapped_column(String())
    relevant_documents: Mapped[str] = mapped_column(String())

    def __repr__(self) -> str:
        return f"Query(id={self.id!r}, query={self.query!r}, relevant_documents={self.relevant_documents!r})"
