from typing import Optional

import strawberry
from goldenCircle.graphql_services.context import Context
from .todo_crud import create_todo
from .todo_schemas import TodoCreate
from .todo_types import Todo


# Define GraphQL mutations
@strawberry.type
class TodoMutation:
    @strawberry.mutation
    async def createTodo(
            self, info: strawberry.Info[Context], title: str, description: Optional[str] = None) -> Todo:
        todo_create = TodoCreate(title=title, description=description)
        db = info.context.db
        todo = await create_todo(db, todo_create)
        return todo
