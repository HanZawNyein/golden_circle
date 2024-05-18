import strawberry
from fastapi import HTTPException
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from graphql_services.context import get_context, Context
from auth.crud import create_user, authenticate_user, get_user_by_username, request_password_reset, reset_password, \
    change_password
from auth.token import create_access_token, verify_password

from .types import User, Token


# Define GraphQL mutations
@strawberry.type
class AuthenticationMutation:
    @strawberry.mutation
    async def register(self, username: str, password: str, info: strawberry.Info[Context]) -> User:
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

    @strawberry.mutation
    async def changePassword(self, new_password: str, info: strawberry.Info[Context]) -> str:
        db: AsyncSession = info.context.db
        user_id = info.context.user
        user = await change_password(db, user_id, new_password)
        print(user,user_id,db)
        if user:
            return "Password Change Successfully."
        else:
            raise ValueError("User not found")

    @strawberry.mutation
    async def requestPasswordReset(self, username: str, info: strawberry.Info[Context]) -> str:
        db: AsyncSession = info.context.db
        user = request_password_reset(db, username)
        if user:
            return "Password reset email sent"
        else:
            raise ValueError("User not found")

    @strawberry.mutation
    async def resetPassword(self, username: str, info: strawberry.Info[Context]) -> str:
        db: AsyncSession = info.context.db
        user = reset_password(db, username, reset_token='112', new_password='122')
        if user:
            return "Password reset email sent"
        else:
            raise ValueError("User not found")
