from typing import Optional

from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = None