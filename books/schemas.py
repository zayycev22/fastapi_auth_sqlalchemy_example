from pydantic import BaseModel, Field
from fastapi_auth.schemas import AbstractDefaultSchema, schema_detail_type


class BookCreate(BaseModel):
    name: str = Field(max_length=100, min_length=2)


class ArticleCreate(BaseModel):
    name: str = Field(max_length=100, min_length=2)


class BookResponseErrorSchema(AbstractDefaultSchema[schema_detail_type]):
    status: str = Field(default="Error")
    detail: schema_detail_type


class BookResponseOK(AbstractDefaultSchema[schema_detail_type]):
    status: str = Field(default="OK")
    detail: schema_detail_type
