import datetime
from typing import Optional

from fastapi_auth.serializers import Serializer

from books.models import Book, Article
from fastapi_auth.sqlalchemy_models.serializers import ModelSerializer


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class BookSerializer(Serializer):
    author: str
    article: Optional[ArticleSerializer.response_schema()] = ArticleSerializer
    time_created: datetime.datetime

    async def get_author(self, instance: Book) -> str:
        user = await instance.awaitable_attrs.author
        return user.email

    async def get_article(self, instance: Book) -> Optional[Article]:
        article = await instance.awaitable_attrs.article
        return article

    async def get_time_created(self, instance: Book):
        return instance.time_created.strftime('%Y-%m-%dT%H:%M:%S.%f')
