from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_auth.filters import OrderingFilter
from fastapi_auth.permissions import IsAuthenticated
from tortoise.exceptions import DoesNotExist, IntegrityError
from auth.models import User
from books.models import Book, Article
from books.schemas import BookCreate, ArticleCreate, BookResponseErrorSchema, BookResponseOK
from books.serializers import BookSerializer
from fastapi_auth.schemas import DefaultSchema
from pagination import DefaultLimitOffsetPagination
from search_filter import TortoiseSearchFilter

book_router = APIRouter(prefix="/books")


@book_router.post("/create", dependencies=[Depends(IsAuthenticated())], status_code=201,
                  response_model=DefaultSchema[str], responses={201: {"model": DefaultSchema[str]}})
async def create_book(request: Request, book_data: BookCreate):
    user: User = request.user
    await Book.create(name=book_data.name, author=user)
    return JSONResponse({"status": "OK", "detail": "Book created"}, status_code=201)


@book_router.get("/", dependencies=[Depends(IsAuthenticated()), Depends(DefaultLimitOffsetPagination.request_schema()),
                                    Depends(OrderingFilter.request_schema()),
                                    Depends(TortoiseSearchFilter.request_schema())],
                 status_code=200, response_model=DefaultLimitOffsetPagination.response_schema(BookSerializer))
async def book_list(request: Request):
    books = await Book.filter(author=request.user).select_related("author")
    searched_data = await TortoiseSearchFilter("article__name", "article__book__name").filter_queryset(request, books)
    filtered_data = await OrderingFilter("name", "id").filter_queryset(request, searched_data)
    return await DefaultLimitOffsetPagination(request=request, serializer=BookSerializer).get_paginated_response(
        filtered_data)


@book_router.get("/{book_id}", dependencies=[Depends(IsAuthenticated())],
                 response_model=DefaultSchema[BookSerializer.response_schema()])
async def book_instance(request: Request, book_id: int):
    user = request.user
    try:
        book = await Book.filter(author=user).get(id=book_id)
    except DoesNotExist:
        return JSONResponse({"status": "error", "detail": "Book does not exists"}, status_code=404)
    else:
        serializer = BookSerializer(instance=book)
        # Note: be careful with JSONResponse, it don`t serialize pydantic models if depth more than 1
        return {"status": "OK", "detail": await serializer.data}


@book_router.post("/{book_id}/change_name", dependencies=[Depends(IsAuthenticated())],
                  response_model=DefaultSchema[str])
async def change_book_name(request: Request, book_id: int, book_data: BookCreate):
    user = request.user
    try:
        book = await Book.filter(author=user).get(id=book_id)
    except DoesNotExist:
        return JSONResponse({"status": "Error", "detail": "Book does not exists"}, status_code=404)
    else:
        book.name = book_data.name
        await book.save()
        return JSONResponse({"status": "OK", "detail": "Name changed"}, status_code=200)


@book_router.post("/article/{book_id}/create", dependencies=[Depends(IsAuthenticated())],
                  response_model=DefaultSchema[str],
                  responses={201: {"model": BookResponseOK[str]}, 404: {"model": BookResponseErrorSchema[str]},
                             400: {"model": BookResponseErrorSchema[str]}})
async def create_article(request: Request, book_id: int, article_data: ArticleCreate):
    try:
        book = await Book.filter(author=request.user).get(id=book_id)
    except DoesNotExist:
        return JSONResponse({"status": "Error", "detail": "Book does not exists"}, status_code=404)
    else:
        try:
            await Article.create(book=book, name=article_data.name)
            return JSONResponse({"status": "OK", "detail": "Article created"}, status_code=201)
        except IntegrityError:
            return JSONResponse({"status": "Error", "detail": "Article already exists"}, status_code=400)
