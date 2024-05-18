from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .todo_models import TodoModel
from .todo_schemas import TodoCreate


async def get_todos(db: AsyncSession, limit: int, offset: int) -> List[TodoModel]:
    result = await db.execute(select(TodoModel).offset(offset).limit(limit))
    return result.scalars().all()


async def get_todo_by_id(db: AsyncSession, todo_id: int):
    result = await db.execute(select(TodoModel).filter(TodoModel.id == todo_id))
    return result.scalars().first()


#
async def create_todo(db: AsyncSession, todo: TodoCreate):
    db_todo = TodoModel(title=todo.title, description=todo.description, completed=todo.completed)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

# async def update_todo(db: AsyncSession, todo_id: int, todo: TodoUpdate):
#     db_todo = await get_todo_by_id(db, todo_id)
#     if db_todo:
#         if todo.title is not None:
#             db_todo.title = todo.title
#         if todo.description is not None:
#             db_todo.description = todo.description
#         if todo.completed is not None:
#             db_todo.completed = todo.completed
#         await db.commit()
#         await db.refresh(db_todo)
#     return db_todo
#
# async def delete_todo(db: AsyncSession, todo_id: int):
#     db_todo = await get_todo_by_id(db, todo_id)
#     if db_todo:
#         await db.delete(db_todo)
#         await db.commit()
#         return True
#     return False
