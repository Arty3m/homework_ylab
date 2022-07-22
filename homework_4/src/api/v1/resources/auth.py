from datetime import timedelta
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import FreshTokenRequired
from src.api.v1.schemas import UserBase, UserCreate, UserListResponse, UserReqInfo, UserLogin
from src.services import UserService, get_user_service, JwtCache
from src.core.config import JWT_ALGORITHM

from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = 'foo'
    authjwt_algorithm: str = JWT_ALGORITHM


@AuthJWT.load_config
def get_config():
    return Settings()


refresh_expire_time: timedelta = timedelta(days=30)
access_expire_time: timedelta = timedelta(minutes=5)

router = APIRouter()


@router.post(
    path="/signup",
    summary="Добавить пользователя",
    tags=["users"],
    status_code=201
)
def signup(user: UserCreate, user_service: UserService = Depends(get_user_service)) -> dict:
    user: dict = user_service.create_user(user=user)
    if not user:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="user with same username already exist")

    info: dict = {"msg": "User created.", "user": UserReqInfo(**user)}
    return info


@router.post(
    path="/login",
    summary="Войти",
    tags=["users"]
)
def login(user: UserLogin, jwt_cache: JwtCache = Depends(), authorize: AuthJWT = Depends(),
          user_service: UserService = Depends(get_user_service)) -> dict:
    data: dict = user_service.login_user(user=user)
    if not data:
        raise HTTPException(status_code=401, detail='Invalid username or password')

    user_data: UserReqInfo = UserReqInfo(**data)

    refresh_token: str = authorize.create_refresh_token(subject=str(user_data.uuid), expires_time=refresh_expire_time)
    refresh_uuid: str = authorize.get_raw_jwt(refresh_token)['jti']
    another_claims: dict = make_user_claims(user_data, refresh_uuid)

    access_token: str = authorize.create_access_token(subject=str(user_data.uuid), user_claims=another_claims,
                                                      expires_time=access_expire_time)

    jwt_cache.add_to_active_refresh(str(user_data.uuid), refresh_uuid)
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


@router.get(
    path="/users/me",
    summary="Посмотреть профиль",
    tags=["users"])
def profile(jwt_cache: JwtCache = Depends(), authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        jwt_cache.is_active_access_token(authorize.get_jwt_subject(), authorize.get_raw_jwt()["jti"])
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")
    current_user: dict = authorize.get_raw_jwt()

    return {"user": {"username": current_user["username"], "uuid": current_user["sub"],
                     "email": current_user["email"], "is_superuser": current_user["is_superuser"],
                     "created_at": current_user["created_at"], "roles": current_user["roles"]}
            }


@router.patch(
    path="/users/me",
    summary="Обновить информацию профиля",
    tags=["users"]
)
def profile(user: UserBase, jwt_cache: JwtCache = Depends(), user_service: UserService = Depends(get_user_service),
            authorize: AuthJWT = Depends()) -> dict:
    try:
        authorize.jwt_required()
        jwt_cache.is_active_access_token(authorize.get_jwt_subject(), authorize.get_raw_jwt()["jti"])
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")

    curr_user: dict = authorize.get_raw_jwt()
    data: dict = user_service.update_user(user=user, uuid=curr_user["sub"])
    user_data: UserReqInfo = UserReqInfo(**data)
    refresh_uuid: str = curr_user['jti']
    another_claims: dict = make_user_claims(user_data, refresh_uuid)
    access_token: str = authorize.create_access_token(subject=str(user_data.uuid), user_claims=another_claims,
                                                      expires_time=access_expire_time)
    upd: dict = {"msg": "Update is successful. Please use new access_token.", "user": user_data,
                 "access_token": access_token}
    return upd


@router.post(
    path="/refresh",
    summary="Обновить токен",
    tags=["refresh"]
)
def refresh(jwt_cache: JwtCache = Depends(), authorize: AuthJWT = Depends(),
            user_service: UserService = Depends(get_user_service)) -> dict:
    try:
        authorize.jwt_refresh_token_required()
        jwt_cache.is_active_refresh_token(authorize.get_jwt_subject(), authorize.get_raw_jwt()["jti"])
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")

    curr_uuid: str = authorize.get_jwt_subject()
    data: dict = user_service.get_data_by_uuid(curr_uuid)
    user_data: UserReqInfo = UserReqInfo(**data)

    refresh_token: str = authorize.create_refresh_token(subject=str(user_data.uuid), expires_time=refresh_expire_time)
    refresh_uuid: str = authorize.get_raw_jwt(refresh_token)['jti']
    another_claims: dict = make_user_claims(user_data, refresh_uuid)

    access_token: str = authorize.create_access_token(subject=str(user_data.uuid), user_claims=another_claims,
                                                      expires_time=access_expire_time)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post(
    path="/logout",
    summary="Выйти из аккаунта",
    tags=["logout"]
)
def logout(jwt_cache: JwtCache = Depends(), authorize: AuthJWT = Depends()) -> dict:
    try:
        authorize.jwt_required()
        jwt_cache.is_active_access_token(authorize.get_jwt_subject(), authorize.get_raw_jwt()["jti"])
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")
    uuid = authorize.get_jwt_subject()
    access_jti = authorize.get_raw_jwt()["jti"]
    refresh_jti = authorize.get_raw_jwt()["refresh_uuid"]

    jwt_cache.logout(uuid, access_jti, refresh_jti)
    return {"msg": "You have been logged out."}


@router.post(
    path="/logout_all",
    summary="Завершить все сеансы",
    tags=["logout"]
)
def logout_all(jwt_cache: JwtCache = Depends(), authorize: AuthJWT = Depends()) -> dict:
    try:
        authorize.jwt_required()
        jwt_cache.is_active_access_token(authorize.get_jwt_subject(), authorize.get_raw_jwt()["jti"])
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")
    uuid = authorize.get_jwt_subject()
    access_jti = authorize.get_raw_jwt()["jti"]

    jwt_cache.logout_all(uuid, access_jti)
    return {"msg": "You have been logout from all devices."}


def make_user_claims(user_data: UserReqInfo, refresh_uuid: str) -> dict:
    another_claims = {"username": user_data.username, "refresh_uuid": refresh_uuid,
                      "email": user_data.email, "is_superuser": user_data.is_superuser,
                      "created_at": str(user_data.created_at), "roles": user_data.roles}
    return another_claims
