from auth.models import User
from .interfaces.repository_interface import CommentsRepositoryInterface
from starlette import status
from fastapi.responses import Response
from .schemas import CommentSchema


class CommentsService:
    def __init__(self, repository: CommentsRepositoryInterface):
        self._repository = repository

    async def write_comment(self, text: str, article_id: int, user: User) -> CommentSchema:
        return await self._repository.write_comment(article_id=article_id, text=text, user=user)

    async def delete_comment(self, comment_id: int, user: User):
        await self._repository.delete_comment(comment_id=comment_id, user=user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def get_all_comments_from_article(self, article_id: int):
        return await self._repository.get_all_comments_from_article(article_id=article_id)
