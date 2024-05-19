from typing import Optional

import strawberry
from fastapi import HTTPException

from goldenCircle.graphql_services.context import Context
from .todo_crud import create_todo, update_todo, delete_todo
from .todo_models import TodoModel
from .todo_types import Todo, TodoCreate, TodoUpdate


# Define GraphQL mutations
@strawberry.type
class TodoMutation:
    @strawberry.mutation
    async def create_todo(
            self, info: strawberry.Info[Context], title: str, description: Optional[str] = None,
            completed: bool = False) -> Todo:
        db = info.context.db
        todo = await create_todo(db, title=title, description=description, completed=completed)
        return todo

    @strawberry.mutation
    async def update_todo(
            self,
            info: strawberry.Info[Context],
            id: int,
            title: Optional[str] = None,
            description: Optional[str] = None,
            completed: Optional[bool] = None,
    ) -> Optional[Todo]:
        db = info.context.db
        todo = await update_todo(db, id, title=title, description=description, completed=completed)
        return todo

    @strawberry.mutation
    async def delete_todo(
            self, id: int, info: strawberry.Info[Context])-> str:
        db = info.context.db
        todo = await delete_todo(db, id)
        if not todo:
            return "Todo not found."
        return "Todo delete success."
