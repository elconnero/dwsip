from pydantic import BaseModel


class UserResponse(BaseModel):
    sub: str
    email: str | None = None
