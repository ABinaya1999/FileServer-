from fastapi.openapi.models import Schema
from pydantic import BaseModel


class UserSchema(Schema):
    email: str
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published_at: bool = True


class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass