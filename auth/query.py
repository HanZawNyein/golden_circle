import strawberry
from typing import List
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession
from .types import User
# Define GraphQL queries
@strawberry.type
class AuthenticationQuery:
    @strawberry.field
    def profile(self) -> User:
        return User(id=1,username="admin")