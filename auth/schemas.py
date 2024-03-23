from pydantic import BaseModel, Field
from fastapi_auth.schemas import DefaultSchema, schema_detail_type


class UserData(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    email: str
    password: str


class UserErrorSchema(DefaultSchema[schema_detail_type]):
    status: str = Field(default="Error")
    detail: schema_detail_type


class UserOkSchema(DefaultSchema[schema_detail_type]):
    status: str = Field(default="OK")
    detail: schema_detail_type


class AuthResponse(BaseModel):
    status: str = Field(default="OK")
    token: str
