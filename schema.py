import strawberry
from typing import List

from fastapi import HTTPException
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from auth.context import get_context, Context
from auth.crud import create_user, authenticate_user
from auth.token import create_access_token


# Define Strawberry types
@strawberry.type
class User:
    id: int
    username: str


@strawberry.type
class TodoItem:
    id: int
    title: str
    description: str
    owner: User


@strawberry.type
class Token:
    access_token: str
    token_type: str


# Define GraphQL queries
@strawberry.type
class Query:
    @strawberry.field
    async def todos(self, info: Info) -> List[TodoItem]:
        db: AsyncSession = info.context.db
        user_id = info.context.user
        # todos = await get_todos(db, user_id)
        return [
            # TodoItem(
            #     id=todo.id, title=todo.title, description=todo.description,
            #     owner=User(id=todo.owner.id, username=todo.owner.username)
            # ) for todo in todos
        ]


# Define GraphQL mutations
@strawberry.type
class Mutation:
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


# Create GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
