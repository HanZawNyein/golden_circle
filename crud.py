from sqlalchemy.future import select
from sqlalchemy.orm import Session
from models import User, TodoItem
from auth import get_password_hash, verify_password

async def get_user_by_username(db: Session, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()

async def create_user(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: Session, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_todos(db: Session, user_id: int):
    result = await db.execute(select(TodoItem).filter(TodoItem.owner_id == user_id))
    return result.scalars().all()

async def create_todo_item(db: Session, title: str, description: str, user_id: int):
    todo_item = TodoItem(title=title, description=description, owner_id=user_id)
    db.add(todo_item)
    await db.commit()
    await db.refresh(todo_item)
    return todo_item

async def update_todo_item(db: Session, todo_id: int, title: str, description: str):
    result = await db.execute(select(TodoItem).filter(TodoItem.id == todo_id))
    todo_item = result.scalars().first()
    if todo_item:
        todo_item.title = title
        todo_item.description = description
        await db.commit()
        await db.refresh(todo_item)
    return todo_item

async def delete_todo_item(db: Session, todo_id: int):
    result = await db.execute(select(TodoItem).filter(TodoItem.id == todo_id))
    todo_item = result.scalars().first()
    if todo_item:
        await db.delete(todo_item)
        await db.commit()
    return todo_item
