from fastapi import APIRouter, Depends, Request
from fastapi_auth.backends import Backend
from fastapi_auth.exceptions import UserAlreadyExists
from fastapi_auth.filters import OrderingFilter
from fastapi_auth.managers import Manager
from fastapi_auth.permissions import IsAuthenticated, AllowAny
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from auth.backend import get_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import AuthResponse, UserErrorSchema, UserData, UserOkSchema, UserCreate
from auth.serializers import UserSerializer
from db import get_async_session
from pagination import DefaultLimitOffsetPagination

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", response_model=AuthResponse, responses={400: {"model": UserErrorSchema}})
async def auth(user_data: UserData, backend: Backend = Depends(get_backend)) -> JSONResponse:
    user = await backend.authenticate(email=user_data.email, password=user_data.password)
    if user is None:
        return JSONResponse({"status": "Error", "detail": "Invalid login or password"}, status_code=400)
    token = await backend.get_token_by_user(user)
    return JSONResponse({"status": "OK", "token": token}, status_code=200)


@auth_router.get("/me", dependencies=[Depends(IsAuthenticated())], response_model=UserSerializer.response_schema())
async def me(request: Request):
    user: User = request.user
    return await UserSerializer(user).data


@auth_router.post("/register", dependencies=[Depends(AllowAny())],
                  responses={201: {"model": UserOkSchema[str]}, 400: {"model": UserErrorSchema[str]}})
async def register(data: UserCreate, user_manager: Manager = Depends(get_user_manager)):
    try:
        await user_manager.create_user(email=data.email, password=data.password)
    except UserAlreadyExists:
        return JSONResponse({"status": "Error", "detail": "User already exists"}, status_code=400)
    else:
        return JSONResponse({"status": "OK", "detail": "User created"}, status_code=201)


@auth_router.get("/users", dependencies=[Depends(AllowAny()), Depends(DefaultLimitOffsetPagination.request_schema()),
                                         Depends(OrderingFilter.request_schema())],
                 response_model=DefaultLimitOffsetPagination.response_schema(user_schema=UserSerializer))
async def users(request: Request, session: AsyncSession = Depends(get_async_session)):
    data = await session.execute(select(User))
    clients = data.scalars().all()
    filtered_data = await OrderingFilter("id", "email").filter_queryset(request, clients)
    paginator = DefaultLimitOffsetPagination(serializer=UserSerializer, request=request)
    data = await paginator.get_paginated_response(filtered_data)
    return data
