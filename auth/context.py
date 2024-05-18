from functools import cached_property
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
            payload = decode_access_token(token)
            if payload:
                self.request.state.user = payload.get("sub")

        return int(self.request.state.user)

    @cached_property
    def db(self):
        if not self.request:
            return None
        return self.request.state.db


async def get_context() -> Context:
    return Context()

