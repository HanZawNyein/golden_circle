from typing import Optional

import strawberry


# Define Strawberry types
@strawberry.type
class Todo:
    id: int
    title: str
    description: Optional[str]
    completed: bool

@strawberry.type
class TodoCreate:
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = None

@strawberry.type
class TodoUpdate:
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None