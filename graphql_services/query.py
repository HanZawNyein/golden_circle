import strawberry
from auth.query import AuthenticationQuery


@strawberry.type
class Query:
    auth: AuthenticationQuery = strawberry.field(lambda: AuthenticationQuery())
