from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    email: str


class PasswordChangeRequest(BaseModel):
    username: str
    current_password: str
    new_password: str


class TokenRequest(BaseModel):
    username: str
    password: str
