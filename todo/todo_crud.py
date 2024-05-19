from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .todo_models import TodoModel
from .todo_types import TodoCreate, TodoUpdate


async def get_todos(db: AsyncSession, limit: int, offset: int) -> List[TodoModel]:
    result = await db.execute(select(TodoModel).offset(offset).limit(limit))
    return result.scalars().all()


async def get_todo_by_id(db: AsyncSession, todo_id: int):
    result = await db.execute(select(TodoModel).filter(TodoModel.id == todo_id))
    return result.scalars().first()

async def create_todo(db: AsyncSession, **kwargs):
    db_todo = TodoModel(**kwargs)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

async def update_todo(db: AsyncSession, todo_id: int, **todo):
    db_todo = await get_todo_by_id(db, todo_id)
    if db_todo:
        for attr, value in todo.items():
            if value is not None and hasattr(db_todo, attr):
                setattr(db_todo, attr, value)
        await db.commit()
        await db.refresh(db_todo)
    return db_todo



async def delete_todo(db: AsyncSession, todo_id: int):
    db_todo = await get_todo_by_id(db, todo_id)
    if db_todo:
        await db.delete(db_todo)
        await db.commit()
        return True
    return False
