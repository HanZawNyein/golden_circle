import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import User as UserModel, TodoItem as TodoItemModel
from crud import create_user, authenticate_user, get_todos, create_todo_item, update_todo_item, delete_todo_item
from auth import create_access_token, decode_access_token


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


@strawberry.type
class Query:
    @strawberry.field
    async def todos(self, info) -> list[TodoItem]:
        db: AsyncSession = info.context["db"]
        user_id = info.context["user_id"]
        todos = await get_todos(db, user_id)
        return [TodoItem(id=todo.id, title=todo.title, description=todo.description,
                         owner=User(id=todo.owner.id, username=todo.owner.username)) for todo in todos]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register(self, username: str, password: str, info) -> User:
        db: AsyncSession = info.context["db"]
        user = await create_user(db, username, password)
        return User(id=user.id, username=user.username)

    @strawberry.mutation
    async def login(self, username: str, password: str, info) -> Token:
        db: AsyncSession = info.context["db"]
        user = await authenticate_user(db, username, password)
        if not user:
            raise Exception("Invalid credentials")
        access_token = create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")

    @strawberry.mutation
    async def create_todo_item(self, title: str, description: str, info) -> TodoItem:
        db: AsyncSession = info.context["db"]
        user_id = info.context["user_id"]
        todo_item = await create_todo_item(db, title, description, user_id)
        return TodoItem(id=todo_item.id, title=todo_item.title, description=todo_item.description,
                        owner=User(id=todo_item.owner.id, username=todo_item.owner.username))

    @strawberry.mutation
    async def update_todo_item(self, id: int, title: str, description: str, info) -> TodoItem:
        db: AsyncSession = info.context["db"]
        todo_item = await update_todo_item(db, id, title, description)
        return TodoItem(id=todo_item.id, title=todo_item.title, description=todo_item.description,
                        owner=User(id=todo_item.owner.id, username=todo_item.owner.username))

    @strawberry.mutation
    async def delete_todo_item(self, id: int, info) -> bool:
        db: AsyncSession = info.context["db"]
        await delete_todo_item(db, id)
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
