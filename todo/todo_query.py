import strawberry

from goldenCircle.database import operations
from goldenCircle.graphql_services.context import Context
from .todo_models import TodoModel
from .todo_types import Todo


# Define GraphQL queries
@strawberry.type
class TodoQuery:
    @strawberry.field
    async def all_todos(self, info: strawberry.Info[Context], limit: int = 10, offset: int = 0) -> list[Todo]:
        todos = await operations.readAll(info.context.db, limit, offset, ModelClass=TodoModel)
        return todos

    @strawberry.field
    async def get_todo_by_id(self, id: int, info: strawberry.Info[Context]) -> Todo:
        todo = await operations.readById(info.context.db, id, ModelClass=TodoModel)
        return todo
