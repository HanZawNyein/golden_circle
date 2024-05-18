import os

from strawberry.fastapi import GraphQLRouter
from strawberry.schema import Schema
from .context import get_context
from .query import Query
from .mutation import Mutation
# Create GraphQL schema
schema = Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context, debug=True)
