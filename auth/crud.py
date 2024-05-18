from sqlalchemy.future import select
from sqlalchemy.orm import Session
from auth.models import User
from auth.token import (get_password_hash, verify_password)

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