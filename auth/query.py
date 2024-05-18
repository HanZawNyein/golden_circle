import strawberry
from typing import List
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession

from .context import Context
from .types import User


# Define GraphQL queries
@strawberry.type
class AuthenticationQuery:
    @strawberry.field
    def profile(self, info: strawberry.Info[Context]) -> User:
        db: AsyncSession = info.context.db
        user_id = info.context.user
        return User(id=1, username="admin")
