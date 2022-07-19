from datetime import datetime
import uuid as uuid_pkg
from sqlmodel import Field, SQLModel


__all__ = ("User",)


class User(SQLModel, table=True):
    uuid: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True, nullable=False)
    roles: list = Field(default=[])
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
