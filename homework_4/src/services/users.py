from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlmodel import Session

from src.api.v1.schemas.auth import UserCreate, UserReqInfo, UserLogin, UserBase
from src.db import AbstractCache, get_cache, get_session
from src.models import User
from src.services import ServiceMixin

__all__ = ("UserService", "get_user_service")


class UserService(ServiceMixin):
    def get_user_list(self) -> dict:
        """Получить список пользователей."""
        users = self.session.query(User).order_by(User.created_at).all()
        return {"users": [UserReqInfo(**user.dict()) for user in users]}

    def create_user(self, user: UserCreate) -> Optional[dict]:
        """Создать пользователя."""
        new_user = User(username=user.username, email=user.email, password=user.password)
        if self.session.query(User).filter(User.username == user.username).first():
            return None
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user.dict()

    def update_user(self, user: UserBase, uuid: str):
        updated_user: User = self.session.query(User).filter(User.uuid == uuid).first()
        updated_user.username = user.username
        updated_user.email = user.email
        self.session.add(updated_user)
        self.session.commit()
        self.session.refresh(updated_user)
        return updated_user.dict()

    def login_user(self, user: UserLogin) -> Optional[dict]:
        if (data := self.session.query(User).filter(User.username == user.username).filter(
                User.password == user.password).first()):
            return data.dict()
        return None

    def get_data_by_uuid(self, uuid: str):
        data = self.session.query(User).filter(User.uuid == uuid).first()
        return data.dict()


# get_post_service — это провайдер UserService. Синглтон
@lru_cache()
def get_user_service(
        cache: AbstractCache = Depends(get_cache),
        session: Session = Depends(get_session),
) -> UserService:
    return UserService(cache=cache, session=session)
