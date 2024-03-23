from fastapi import Depends
from fastapi_auth.managers import Manager
from fastapi_auth_sqlalchemy_models import UserRepository

from auth.models import get_user_repository, User


async def get_user_manager(user_repo: UserRepository = Depends(get_user_repository)):
    yield Manager[User, UserRepository](repo=user_repo)
