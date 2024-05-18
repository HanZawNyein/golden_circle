import strawberry
from typing import List

from fastapi import HTTPException
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from graphql_services.context import get_context, Context
from auth.crud import create_user, authenticate_user
from auth.token import create_access_token


# Define Strawberry types
@strawberry.type
class User:
    id: int
    username: str



@strawberry.type
class Token:
    access_token: str
    token_type: str