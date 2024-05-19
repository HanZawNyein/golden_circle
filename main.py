from fastapi import FastAPI

from goldenCircle.database.events import start_db
from goldenCircle.database.middleware import AddDbToRequestMiddleware
from goldenCircle.graphql_services import graphql_app

# Replace the mutation schema with the updated Mutation class
# graphql_app.schema.mutation.todo = strawberry.mutation(lambda: TodoMutation())
# graphql_app.schema.query.todo: TodoQuery = strawberry.field(lambda: TodoQuery())

app = FastAPI()

app.add_middleware(AddDbToRequestMiddleware)
app.add_event_handler("startup", start_db)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"message": "Welcome from Golden Circle!"}
