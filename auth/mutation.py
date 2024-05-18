import strawberry
from fastapi import HTTPException
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from auth.context import get_context, Context
from auth.crud import create_user, authenticate_user
from auth.token import create_access_token

from .types import User,Token

# Define GraphQL mutations
@strawberry.type
class AuthenticationMutation:
    @strawberry.mutation
    async def register(self, username: str, password: str, info: Info) -> User:
        db: AsyncSession = info.context.db
        user = await create_user(db, username, password)
        return User(id=user.id, username=user.username)

    @strawberry.mutation
    async def login(self, username: str, password: str, info: strawberry.Info[Context]) -> Token:
        db: AsyncSession = info.context.db
        user = await authenticate_user(db, username, password)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, token_type="bearer")