from functools import cached_property

from passlib.exc import InvalidTokenError
from strawberry.fastapi import BaseContext

from auth.token import decode_access_token


class Context(BaseContext):
    @cached_property
    def user(self):
        if not self.request:
            return None

        authorization = self.request.headers.get("Authorization", None)
        if authorization:
            token = authorization.replace("Bearer ", "")
            try:
                payload = decode_access_token(token)
                if payload:
                    user_id = payload.get("sub")
                    self.request.state.user = user_id
                    return int(user_id)
            except InvalidTokenError as e:
                # Handle invalid token error
                # Return a default user ID or raise an error if user information is required
                # return DEFAULT_USER_ID
                # or
                # raise ValueError("Authorization header or token payload is missing")
                return None

    @cached_property
    def db(self):
        if not self.request:
            return None
        return self.request.state.db


async def get_context() -> Context:
    return Context()
