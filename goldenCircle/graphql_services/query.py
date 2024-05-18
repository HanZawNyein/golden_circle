import strawberry

from auth.query import AuthenticationQuery
from todo.todo_query import TodoQuery


@strawberry.type
class Query:
    auth: AuthenticationQuery = strawberry.field(lambda: AuthenticationQuery())
    todo: TodoQuery = strawberry.field(lambda: TodoQuery())
