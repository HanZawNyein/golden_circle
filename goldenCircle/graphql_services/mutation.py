import strawberry

from auth.mutation import AuthenticationMutation
from todo.todo_mutation import TodoMutation

@strawberry.type
class Mutation:
    auth: AuthenticationMutation = strawberry.mutation(lambda: AuthenticationMutation())
    todo: TodoMutation = strawberry.mutation(lambda: TodoMutation())