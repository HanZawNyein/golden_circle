from typing import Any, Dict

import strawberry


@strawberry.input
class FieldInput:
    fields: Dict[str, Any]
