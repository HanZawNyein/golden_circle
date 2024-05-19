from typing import Optional

import strawberry

from goldenCircle.database import operations
from goldenCircle.graphql_services.context import Context

from .todo_models import TodoModel
from .todo_types import Todo


# Define GraphQL mutations
@strawberry.type
class TodoMutation:
    @strawberry.mutation
    async def create_todo(
            self, info: strawberry.Info[Context],
            title: str,
            description: Optional[str] = None,
            completed: bool = False) -> Todo:
        kwargs = {
            "title": title,
            "description": description,
            "completed": completed,
        }
        todo = await operations.create(info.context.db, TodoModel, **kwargs)
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
        kwargs = {
            "title": title,
            "description": description,
            "completed": completed,
        }
        todo = await operations.write(info.context.db, db_id=id, ModelClass=TodoModel, **kwargs)
        return todo

    @strawberry.mutation
    async def delete_todo(
            self, id: int, info: strawberry.Info[Context]) -> str:
        await operations.delete(info.context.db, id,TodoModel)
        return "Todo delete success."
