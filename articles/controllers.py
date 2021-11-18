from endpoint import Endpoint, TagsRoute, PrefixRoute
from .models import Article
from settings_config import ARTICLES_IMAGE_DIR
from image_utils.local_image_service import LocalImageUploadService
from .services import ArticlesServices
from auth.token_service import TokenService
from auth.models import User
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, Response
from typing import Optional
from database import get_db
from .repository import ArticlesRepository
from .schemas import ArticleSchema, CreatedArticleSchema
from permissions import GetUser
from sqlalchemy.ext.asyncio import AsyncSession

articles_router = APIRouter(tags=[TagsRoute.articles], prefix=PrefixRoute.articles)


@articles_router.get(Endpoint.user_articles, response_model=list[ArticleSchema])
async def get_user_articles(user_id: int, offset: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)) -> list[Article]:
    return await ArticlesServices(repository=ArticlesRepository(session=db)).get_user_articles(offset=offset, limit=limit,
                                                                                               user_id=user_id)


@articles_router.get(Endpoint.slash, status_code=status.HTTP_200_OK, response_model=list[ArticleSchema])
async def get_all_articles(offset: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)) -> list[Article]:
    return await ArticlesServices(repository=ArticlesRepository(session=db)).get_all_articles(offset=offset, limit=limit)


@articles_router.get(Endpoint.single_article, response_model=ArticleSchema, status_code=status.HTTP_200_OK)
async def get_single_article(article_id: int, db: AsyncSession = Depends(get_db)) -> Article:
    return await ArticlesServices(repository=ArticlesRepository(session=db)).get_single_article(article_id=article_id)


@articles_router.put(Endpoint.single_article, status_code=status.HTTP_200_OK, response_model=ArticleSchema)
async def update_article(article_id: int, title: str = Form(None), content: str = Form(None),
                         files: list[UploadFile] = File(None), db: AsyncSession = Depends(get_db),
                         user: User = Depends(GetUser(token_service=TokenService()))) -> Article:
    return await ArticlesServices(repository=ArticlesRepository(session=db)) \
        .update_article(user=user, article_id=article_id, title=title, content=content, files=files,
                        file_service=LocalImageUploadService())


@articles_router.delete(Endpoint.single_article)
async def delete_article(article_id: int, db: AsyncSession = Depends(get_db),
                         user: User = Depends(GetUser(token_service=TokenService()))):
    return await ArticlesServices(repository=ArticlesRepository(session=db)).delete_article(article_id=article_id, user=user)


@articles_router.post(Endpoint.slash, status_code=status.HTTP_201_CREATED, response_model=CreatedArticleSchema)
async def create_article(user: User = Depends(GetUser(token_service=TokenService())), title: str = Form(..., max_length=255),
                         content: str = Form(...), files: Optional[list[UploadFile]] = File(None),
                         db: AsyncSession = Depends(get_db)) -> Article:
    return await ArticlesServices(repository=ArticlesRepository(session=db)) \
        .create_article(file_service=LocalImageUploadService(), user=user, title=title, content=content, files=files)


@articles_router.get(Endpoint.image)
async def get_image(filename: str, db: AsyncSession = Depends(get_db)):
    image = await ArticlesServices(repository=ArticlesRepository(session=db)) \
        .get_image(filename=filename, file_service=LocalImageUploadService(), folder=ARTICLES_IMAGE_DIR)
    return Response(content=image, status_code=200)


@articles_router.delete(Endpoint.image)
async def delete_image(filename: str, db: AsyncSession = Depends(get_db),
                       user: User = Depends(GetUser(token_service=TokenService()))):
    return await ArticlesServices(repository=ArticlesRepository(session=db)) \
        .delete_image(folder=ARTICLES_IMAGE_DIR, image_name=filename, user=user, file_service=LocalImageUploadService())
