from fastapi.openapi.models import Schema


class UserSchema(Schema):
    email: str
    password: str

