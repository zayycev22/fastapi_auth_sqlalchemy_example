from fastapi import Depends
from fastapi_auth.sqlalchemy_models import Token, EmailUser, UserRepository, TokenRepository
from fastapi_auth.strategies import DbStrategy
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session, Base


class User(EmailUser, Base):
    __tablename__ = "user"


class AccessToken(Token, Base):
    __tablename__ = "token"


async def get_user_repository(session: AsyncSession = Depends(get_async_session)):
    yield UserRepository(session=session, user_m=User)


async def get_token_repository(session: AsyncSession = Depends(get_async_session)):
    yield TokenRepository(session=session, tp=AccessToken)


async def get_db_strategy(
        user_repo: UserRepository = Depends(get_user_repository),
        token_repo: TokenRepository = Depends(get_token_repository)
) -> DbStrategy:
    yield DbStrategy(user_repo=user_repo, token_repo=token_repo)
