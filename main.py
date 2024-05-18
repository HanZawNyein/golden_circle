from graphql_services import graphql_app
from fastapi import FastAPI
from database.middleware import AddDbToRequestMiddleware
from database.events import start_db
from typing import Type

app = FastAPI()

app.add_middleware(AddDbToRequestMiddleware)
app.add_event_handler("startup", start_db)


@app.get("/")
async def root():
    return {"message": "Welcome from Golden Circle!"}


app.include_router(graphql_app, prefix="/graphql")