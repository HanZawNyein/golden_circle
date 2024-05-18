from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth.models import User
from auth.token import (get_password_hash, verify_password)


async def get_user_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(User).filter(User.id == id))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def create_user(db: AsyncSession, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


async def change_password(db: AsyncSession, user_id: int, new_password: str)->bool:
    user = await get_user_by_id(db, user_id)
    if user:
        user.hashed_password = get_password_hash(new_password)
        await db.commit()
        return True
    return False


async def request_password_reset(db: AsyncSession, username: str)->bool:
    user = await get_user_by_username(db, username)
    if user:
        # Implement logic to send password reset email
        # For example, generate a unique token and send it to the user's email
        # Then update the user's database record with the token
        # user.reset_token = generate_reset_token()
        # await db.commit()
        return True
    return False


async def reset_password(db: AsyncSession, username: str, reset_token: str, new_password: str)->bool:
    user = await get_user_by_username(db, username)
    if user and user.reset_token == reset_token:
        user.hashed_password = get_password_hash(new_password)
        user.reset_token = None  # Clear the reset token
        await db.commit()
        return True
    return False
