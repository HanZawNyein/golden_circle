from typing import Union

import strawberry
from fastapi.exceptions import HTTPException

from goldenCircle.exceptions import ErrorMessage
from goldenCircle.graphql_services.context import Context
from goldenCircle.database import crud as db_crud
from .todo_crud import get_todos, get_todo_by_id
from .todo_models import TodoModel
from .todo_types import Todo



# Define GraphQL queries
@strawberry.type
class TodoQuery:
    @strawberry.field
    async def allTodos(self, info: strawberry.Info[Context], limit: int = 10, offset: int = 0) -> list[Todo]:
        todos = await db_crud.readAll(info.context.db, limit, offset,ModelClass=TodoModel)
        return todos

    @strawberry.field
    async def getTodoById(self, id: int, info: strawberry.Info[Context]) -> Union[Todo | ErrorMessage]:
        db = info.context.db
        todo = await get_todo_by_id(db, id)
        if not todo:
            raise HTTPException(status_code=404, detail="todo not found.")
        return Todo(id=todo.id, title=todo.title, description=todo.description, completed=todo.completed)
