from datetime import datetime
import uuid as uuid_pkg
from pydantic import BaseModel

__all__ = (
    "UserCreate",
    "UserBase",
    "UserReqInfo",
    "UserListResponse",
    "UserLogin",
)


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserReqInfo(UserBase):
    roles: list[str] = []
    created_at: datetime
    is_active: bool
    is_superuser: bool
    uuid: uuid_pkg.UUID


class UserListResponse(BaseModel):
    users: list[UserReqInfo] = []


class UserLogin(BaseModel):
    username: str
    password: str
