from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from src.api.v1.schemas import PostCreate, PostListResponse, PostModel
from src.services import PostService, get_post_service, JwtCache
from src.services import UserService

router = APIRouter()


@router.get(
    path="/",
    response_model=PostListResponse,
    summary="Список постов",
    tags=["posts"],
)
def post_list(
        post_service: PostService = Depends(get_post_service),
) -> PostListResponse:
    posts: dict = post_service.get_post_list()
    if not posts:
        # Если посты не найдены, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="posts not found")
    return PostListResponse(**posts)


@router.get(
    path="/{post_id}",
    response_model=PostModel,
    summary="Получить определенный пост",
    tags=["posts"],
)
def post_detail(
        post_id: int, post_service: PostService = Depends(get_post_service),
) -> PostModel:
    post: Optional[dict] = post_service.get_post_detail(item_id=post_id)
    if not post:
        # Если пост не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="post not found")
    return PostModel(**post)


@router.post(
    path="/",
    response_model=PostModel,
    summary="Создать пост",
    tags=["posts"],
    status_code=201
)
def post_create(post: PostCreate, jwt_cache: JwtCache = Depends(), authorize: AuthJWT = Depends(),
                post_service: PostService = Depends(get_post_service),
                ) -> PostModel:
    try:
        authorize.jwt_required()
        jwt_cache.is_active_access_token(authorize.get_jwt_subject(), authorize.get_raw_jwt()["jti"])
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")

    post: dict = post_service.create_post(post=post)
    return PostModel(**post)
