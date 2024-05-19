from typing import List

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .todo_models import TodoModel


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
            if not hasattr(db_todo, attr):
                raise HTTPException(status_code=404, detail='Attribute does not exist')
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
