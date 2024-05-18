import strawberry

from auth.mutation import AuthenticationMutation


@strawberry.type
class Mutation:
    auth: AuthenticationMutation = strawberry.mutation(lambda: AuthenticationMutation())
