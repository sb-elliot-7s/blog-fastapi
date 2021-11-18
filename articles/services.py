from typing import Optional
from .models import Article
from image_utils.image_utils_interface import FileServiceInterface
from .schemas import ArticleCreateSchema
from auth.models import User
from fastapi import UploadFile, status, HTTPException
from fastapi.responses import Response, JSONResponse
from articles.interfaces.repository_interface import ArticleRepositoryInterface
from message_error import DETAILERROR


class ArticlesServices:
    def __init__(self, repository: ArticleRepositoryInterface):
        self._repository = repository

    async def get_user_articles(self, user_id: int, offset: int, limit: int) -> list[Article]:
        return await self._repository.get_articles_from_user(user_id=user_id, offset=offset, limit=limit)

    async def get_all_articles(self, offset: int, limit: int) -> list[Article]:
        return await self._repository.get_all_articles(offset=offset, limit=limit)

    async def get_single_article(self, article_id: int) -> Article:
        return await self._repository.get_single_article(article_id=article_id)

    async def update_article(self, user: User, article_id: int, title: str, content: str,
                             files: Optional[list[UploadFile]], file_service: FileServiceInterface) -> Article:
        updated_article = ArticleCreateSchema(title=title, content=content).dict(exclude_none=True)
        result, article = await self._repository.update_article(user=user, article_id=article_id, files=files,
                                                                updated_data=updated_article, file_service=file_service)
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=DETAILERROR.CANNOT_UPDATE.article)
        return article

    async def delete_article(self, article_id: int, user: User) -> Response:
        if not (_ := await self._repository.delete_article(article_id=article_id, user=user)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=DETAILERROR.CANNOT_DELETE.article)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def create_article(self, user: User, title: str, content: str, files: Optional[list[UploadFile]],
                             file_service: FileServiceInterface) -> Article:
        article = ArticleCreateSchema(title=title, content=content)
        return await self._repository.create_article_and_save_image(user=user, files=files, article=article,
                                                                    file_service=file_service)

    @staticmethod
    async def get_image(filename: str, folder: str, file_service: FileServiceInterface):
        return await file_service.read_file(filename=filename, folder=folder)

    async def delete_image(self, folder: str, image_name: str, user: User, file_service: FileServiceInterface):
        await self._repository.delete_image(image_name=image_name, user=user)
        await file_service.delete_image(filename=image_name, folder=folder)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
