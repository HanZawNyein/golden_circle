import strawberry


@strawberry.type
class ErrorMessage:
    message: str
