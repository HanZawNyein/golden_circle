from fastapi import FastAPI

from app import graphql_app
from goldenCircle.database.events import start_db
from goldenCircle.database.middleware import AddDbToRequestMiddleware

app = FastAPI()

app.add_middleware(AddDbToRequestMiddleware)
app.add_event_handler("startup", start_db)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"message": "Welcome from Golden Circle!"}
