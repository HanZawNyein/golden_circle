import strawberry

from goldenCircle.graphql_services.context import Context
from goldenCircle.database import crud as db_crud

from .todo_models import TodoModel
from .todo_types import Todo


# Define GraphQL queries
@strawberry.type
class TodoQuery:
    @strawberry.field
    async def all_todos(self, info: strawberry.Info[Context], limit: int = 10, offset: int = 0) -> list[Todo]:
        todos = await db_crud.readAll(info.context.db, limit, offset, ModelClass=TodoModel)
        return todos

    @strawberry.field
    async def get_todo_by_id(self, id: int, info: strawberry.Info[Context]) -> Todo:
        db = info.context.db
        todo = await db_crud.readById(db, id, ModelClass=TodoModel)
        return todo
