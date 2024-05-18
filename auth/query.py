import strawberry
from sqlalchemy.ext.asyncio import AsyncSession

from graphql_services.context import Context
from .crud import get_user_by_id
from .types import User


# Define GraphQL queries
@strawberry.type
class AuthenticationQuery:
    @strawberry.field
    def profile(self, info: strawberry.Info[Context]) -> User:
        db: AsyncSession = info.context.db
        user_id = info.context.user
        user = get_user_by_id(db, id=user_id)
        if not user:
            raise ValueError("User profile not found")
        return user
