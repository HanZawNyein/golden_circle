from typing import Optional

import strawberry

from goldenCircle.graphql_services.context import Context
from .todo_crud import create_todo, update_todo
from .todo_types import TodoCreate, TodoUpdate
from .todo_types import Todo


# Define GraphQL mutations
@strawberry.type
class TodoMutation:
    @strawberry.mutation
    async def createTodo(
            self, info: strawberry.Info[Context], title: str, description: Optional[str] = None,
            completed: bool = False) -> Todo:
        todo_create = TodoCreate(title=title, description=description, completed=completed)
        db = info.context.db
        todo = await create_todo(db, todo_create)
        return todo

    @strawberry.mutation
    async def update_todo(
            self, id: int, info: strawberry.Info[Context], title: Optional[str] = None,
            description: Optional[str] = None,
            completed: Optional[bool] = None,
    ) -> Optional[Todo]:
        db = info.context.db
        todo_update = TodoUpdate(title=title, description=description, completed=completed)
        todo = await update_todo(db, id, todo_update)
        return todo  # Todo.from_orm(todo) if todo else None
