import strawberry

# Define Strawberry types
@strawberry.type
class User:
    id: int
    username: str



@strawberry.type
class Token:
    access_token: str
    token_type: str