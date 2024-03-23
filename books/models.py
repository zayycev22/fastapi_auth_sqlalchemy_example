import datetime

from fastapi_auth.sqlalchemy_models import ExModel
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base
from auth.models import User


class Article(ExModel, Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    book: Mapped['Book'] = relationship(back_populates="article")
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id', ondelete="cascade"), nullable=False)


class Book(ExModel, Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    article: Mapped['Article'] = relationship(back_populates="book", uselist=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='cascade'), nullable=False)
    author: Mapped['User'] = relationship()
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    time_created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
