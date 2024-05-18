from starlette.requests import Request
from schema import graphql_app
from fastapi import FastAPI
from database import SessionLocal, engine, Base
from auth import decode_access_token


app = FastAPI()


@app.middleware("http")
async def add_db_to_request(request: Request, call_next):
    async with SessionLocal() as session:
        request.state.db = session
        response = await call_next(request)
        return response


@app.middleware("http")
async def add_user_to_request(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token:
        token = token.replace("Bearer ", "")
        payload = decode_access_token(token)
        if payload:
            request.state.user_id = payload.get("sub")
    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


app.include_router(graphql_app, prefix="/graphql")
