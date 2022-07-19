from datetime import timedelta
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse

# from src.api.v1.schemas import PostCreate, PostListResponse, PostModel
from src.api.v1.schemas import UserBase, UserCreate, UserListResponse, UserReqInfo, UserModel, UserLogin

from src.services import UserService, get_user_service

from src.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = 'foo'
    authjwt_algorithm: str = JWT_ALGORITHM


@AuthJWT.load_config
def get_config():
    return Settings()


refresh_expire_time = timedelta(days=30)
access_expire_time = timedelta(minutes=5)

router = APIRouter()


@router.post(
    path="/signup",
    response_model=UserModel,
    summary="Добавить пользователя",
    tags=["users"],
    status_code=201
)
def signup(user: UserCreate, user_service: UserService = Depends(get_user_service)) -> UserModel:
    user: dict = user_service.create_user(user=user)
    if not user:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="user with same username already exist")

    ur = {"msg": "User created.", "user": UserReqInfo(**user)}
    return UserModel(**ur)


@router.post(
    path="/login",
    summary="Войти",
    tags=["users"]
)
def login(user: UserLogin, authorize: AuthJWT = Depends(), user_service: UserService = Depends(get_user_service)):
    data: dict = user_service.login_user(user=user)
    if not data:
        raise HTTPException(status_code=401, detail='Invalid username or password')

    user_data = UserReqInfo(**data)

    refresh_token = authorize.create_refresh_token(subject=str(user_data.uuid), expires_time=refresh_expire_time)
    refresh_uuid = authorize.get_raw_jwt(refresh_token)['jti']
    another_claims = make_user_claims(user_data, refresh_uuid)

    access_token = authorize.create_access_token(subject=str(user_data.uuid), user_claims=another_claims,
                                                 expires_time=access_expire_time)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get(
    path="/users",
    summary="Посмотреть всех пользователей",
    tags=["users"]
)
def users(user_service: UserService = Depends(get_user_service)) -> UserListResponse:
    user_list: dict = user_service.get_user_list()
    if not users:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="users not found")
    return UserListResponse(**user_list)


@router.get(path="/users/me")
def profile(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")
    current_user: dict = authorize.get_raw_jwt()

    return {"user": {"username": current_user["username"], "uuid": current_user["sub"],
                     "email": current_user["email"], "is_superuser": current_user["is_superuser"],
                     "created_at": current_user["created_at"], "roles": current_user["roles"]}
            }


@router.patch(path="/users/me")
def profile(user: UserBase, user_service: UserService = Depends(get_user_service), authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")
    curr_user: dict = authorize.get_raw_jwt()
    data: dict = user_service.update_user(user=user, uuid=curr_user["sub"])
    user_data = UserReqInfo(**data)
    refresh_uuid = curr_user['jti']
    another_claims = make_user_claims(user_data, refresh_uuid)
    access_token = authorize.create_access_token(subject=str(user_data.uuid), user_claims=another_claims,
                                                 expires_time=access_expire_time)
    ur = {"msg": "Update is successful. Please use new access_token.", "user": user_data}
    t = UserModel(**ur).dict()
    t.update({"access_token": access_token})
    return t


@router.post(path="/refresh")
def refresh(authorize: AuthJWT = Depends(), user_service: UserService = Depends(get_user_service)):
    try:
        authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")

    curr_uuid: str = authorize.get_jwt_subject()
    data: dict = user_service.get_data_by_uuid(curr_uuid)
    user_data = UserReqInfo(**data)

    refresh_token = authorize.create_refresh_token(subject=str(user_data.uuid), expires_time=refresh_expire_time)
    refresh_uuid = authorize.get_raw_jwt(refresh_token)['jti']
    another_claims = make_user_claims(user_data, refresh_uuid)

    access_token = authorize.create_access_token(subject=str(user_data.uuid), user_claims=another_claims,
                                                 expires_time=access_expire_time)
    return {"access_token": access_token, "refresh_token": refresh_token}


def make_user_claims(user_data, refresh_uuid):
    another_claims = {"username": user_data.username, "refresh_uuid": refresh_uuid,
                      "email": user_data.email, "is_superuser": user_data.is_superuser,
                      "created_at": str(user_data.created_at), "roles": user_data.roles}
    return another_claims
