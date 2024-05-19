from typing import Any, Dict, Optional
import strawberry
from strawberry.types import Info

@strawberry.input
class FieldInput:
    fields: Dict[str, Any]