from typing import Union

import strawberry
from sqlalchemy.ext.asyncio import AsyncSession

from goldenCircle.exceptions import ErrorMessage
from goldenCircle.graphql_services.context import Context
from .crud import get_user_by_id
from .types import User


# Define GraphQL queries
@strawberry.type
class AuthenticationQuery:
    @strawberry.field
    async def profile(self, info: strawberry.Info[Context]) -> Union[User, ErrorMessage]:
        db: AsyncSession = info.context.db
        user_id = info.context.user
        if not user_id:
            return ErrorMessage(message="Token is Invalid or Expired.")
        db_user: User = await get_user_by_id(db, id=user_id)
        if not db_user:
            return ErrorMessage(message="User profile not found.")
        user = User(id=db_user.id, username=db_user.username)
        return user
