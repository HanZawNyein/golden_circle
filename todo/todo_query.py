from typing import Union, List

import strawberry
from fastapi.exceptions import HTTPException

from goldenCircle.exceptions import ErrorMessage
from goldenCircle.graphql_services.context import Context
from .todo_crud import get_todos, get_todo_by_id
from .todo_types import Todo


# Define GraphQL queries
@strawberry.type
class TodoQuery:
    @strawberry.field
    async def allTodos(self, info: strawberry.Info[Context]) -> List[Todo]:
        db = info.context.db
        todos = await get_todos(db)
        return todos
        # return [Todo(**todo.__dict__) for todo in todos]

    @strawberry.field
    async def getTodoById(self, id: int, info: strawberry.Info[Context]) -> Union[Todo | ErrorMessage]:
        db = info.context.db
        todo = await get_todo_by_id(db, id)
        if not todo:
            raise HTTPException(status_code=404, detail="todo not found.")
        return Todo(id=todo.id,title=todo.title,description=todo.description,completed=todo.completed)
