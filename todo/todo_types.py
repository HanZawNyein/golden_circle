from typing import Optional

import strawberry


# Define Strawberry types
@strawberry.type
class Todo:
    id: int
    title: str
    description: Optional[str]
    completed: bool
