import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import APIKeyHeader
from fastapi_auth import FastApiAuth
from fastapi_auth.authenticators import Authenticator
from fastapi_auth.backends import Backend
from fastapi import Request
from auth.backend import get_backend
from auth.router import auth_router
from auth.signals import signal
from books.router import book_router
from db import func_engine, Base

api_key_header = APIKeyHeader(name='Authorization', auto_error=False)
fastapi_auth = FastApiAuth()


async def auth_dependency(backend: Backend = Depends(get_backend)):
    yield Authenticator(backend=backend, token_prefix="Token")


async def process_token(request: Request, token=Depends(api_key_header),
                        authenticator: Authenticator = Depends(auth_dependency)):
    await authenticator.process_token(request=request, raw_token=token)


app = FastAPI(dependencies=[Depends(process_token)])


@app.on_event("startup")
async def startup():
    async with func_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
    fastapi_auth.listen_signals(signal)


app.include_router(auth_router, tags=["authentication"])
app.include_router(book_router, tags=["books"])

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
