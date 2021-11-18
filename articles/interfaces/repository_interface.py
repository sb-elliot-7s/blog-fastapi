from abc import ABC, abstractmethod
from typing import Optional
from articles.models import Article
from image_utils.image_utils_interface import FileServiceInterface
from articles.schemas import ArticleCreateSchema
from fastapi import UploadFile
from auth.models import User


class ArticleRepositoryInterface(ABC):

    @abstractmethod
    async def _get_article_by_id(self, article_id: int) -> Article: pass

    @abstractmethod
    async def get_all_articles(self, offset: int, limit: int) -> list[Article]: pass

    @abstractmethod
    async def get_articles_from_user(self, user_id: int, offset: int, limit: int) -> list[Article]: pass

    @abstractmethod
    async def get_single_article(self, article_id: int) -> Article: pass

    @abstractmethod
    async def update_article(self, user: User, article_id: int, file_service: FileServiceInterface,
                             updated_data: dict, files: Optional[list[UploadFile]] = None) -> tuple[bool, Optional[Article]]: pass

    @abstractmethod
    async def delete_article(self, article_id: int, user: User) -> bool: pass

    @abstractmethod
    async def create_article_and_save_image(self, user: User, article: ArticleCreateSchema,
                                            files: Optional[list[UploadFile]], file_service: FileServiceInterface): pass

    @abstractmethod
    async def delete_image(self, image_name: str, user: User): pass
