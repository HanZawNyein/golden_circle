from strawberry.fastapi import GraphQLRouter
from strawberry.schema import Schema

from todo.todo_mutation import TodoMutation
from .context import get_context
from .mutation import Mutation
from .query import Query

# Create GraphQL schema
schema = Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context, debug=True)
