from fastapi_auth.signals import Signal
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User, AccessToken

signal = Signal()


@signal.after_save(model=User)
async def create_token(instance: User, created: bool, session: AsyncSession):
    if created:
        await AccessToken.create(user_id=instance.id, session=session)
