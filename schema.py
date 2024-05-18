import strawberry
from strawberry.fastapi import GraphQLRouter

from auth.context import get_context
from auth.query import AuthenticationQuery
from auth.types import User
from auth.mutation import AuthenticationMutation
from strawberry.tools import merge_types

queries = AuthenticationQuery,
ComboQuery = merge_types("ComboQuery", queries)

# Create GraphQL schema
schema = strawberry.Schema(query=ComboQuery, mutation=AuthenticationMutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context, debug=True)
