from typing import Optional
import uuid
from sqlalchemy import select, insert, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ArticleCreateSchema
from auth.models import User
from settings_config import ARTICLES_IMAGE_DIR, get_settings
from .models import Article, Image
from fastapi import status, UploadFile, HTTPException
from articles.interfaces.repository_interface import ArticleRepositoryInterface
from image_utils.image_utils_interface import FileServiceInterface
from message_error import DETAILERROR


class ArticlesRepository(ArticleRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self._session = session
        self._settings = get_settings()

    async def _get_article_by_id(self, article_id: int) -> Article:
        res: Result = await self._session.execute(select(Article).filter_by(id=article_id))
        if not (article := res.scalars().first()):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=DETAILERROR.NOT_FOUND.obj('Article'))
        return article

    async def get_articles_from_user(self, user_id: int, offset: int, limit: int) -> list[Article]:
        user: Result = await self._session.execute(select(User).where(User.id == user_id))
        if not user.scalars().first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=DETAILERROR.NOT_FOUND.obj('User'))
        res: Result = await self._session.execute(
            select(Article).where(Article.user_id == user_id).limit(limit).offset(offset))
        return res.scalars().unique().all()

    async def get_all_articles(self, offset: int, limit: int) -> list[Article]:
        res: Result = await self._session.execute(select(Article).limit(limit).offset(offset))
        return res.scalars().unique().all()

    async def get_single_article(self, article_id: int) -> Article:
        return await self._get_article_by_id(article_id=article_id)

    async def _add_images(self, files: Optional[list[UploadFile]], path: str, file_service: FileServiceInterface,
                          article_id: int):
        if files:
            for image in files:
                filename = f'{uuid.uuid4()}:{image.filename}'
                await file_service.write_file(folder=ARTICLES_IMAGE_DIR, file=image, filename=filename)
                await self._session.execute(insert(Image).values(photo=path + filename, article_id=article_id))

    async def create_article_and_save_image(self, user: User, article: ArticleCreateSchema, files: Optional[list[UploadFile]],
                                            file_service: FileServiceInterface):
        res: Result = await self._session.execute(insert(Article).values(**article.dict(), user_id=user.id).returning(Article.id))
        article_id = res.scalars().first()
        await self._add_images(files=files, path=self._settings.articles_image_url, file_service=file_service,
                               article_id=article_id)
        await self._session.commit()
        returned_article: Result = await self._session.execute(select(Article).where(Article.id == article_id))
        return returned_article.scalars().first()

    async def update_article(self, user: User, article_id: int, file_service: FileServiceInterface, updated_data: dict,
                             files: Optional[list[UploadFile]] = None) -> tuple[bool, Optional[Article]]:
        if (article := await self._get_article_by_id(article_id=article_id)) and article.user_id != user.id:
            return False, None
        await self._add_images(files=files, path=self._settings.articles_image_url, file_service=file_service,
                               article_id=article.id)
        await self._session.execute(update(Article).where(Article.id == article.id).values(**updated_data).returning(Article))
        await self._session.commit()
        await self._session.refresh(article)
        return True, article

    async def delete_article(self, article_id: int, user: User) -> bool:
        if (article := await self._get_article_by_id(article_id=article_id)) and (article.user_id != user.id):
            return False
        await self._session.delete(article)
        await self._session.commit()
        return True

    async def delete_image(self, image_name: str, user: User):
        full_path = self._settings.articles_image_url + image_name
        res: Result = await self._session.execute(
            select(Image).join(Article).where(Image.photo == full_path, Article.user_id == user.id))
        if not (image := res.scalars().first()):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=DETAILERROR.NOT_FOUND.obj('Image'))
        await self._session.delete(image)
        await self._session.commit()
