from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from database.base import SessionLocal


class AddDbToRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with SessionLocal() as session:
            request.state.db = session
            response = await call_next(request)
            return response

async def get_db():
    async with SessionLocal() as session:
        yield session