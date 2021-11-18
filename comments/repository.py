from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from articles.models import Article
from auth.models import User
from .interfaces.repository_interface import CommentsRepositoryInterface
from .models import Comment
from fastapi import HTTPException, status
from typing import List
from message_error import DETAILERROR


class CommentRepository(CommentsRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def delete_comment(self, comment_id: int, user: User) -> None:
        res: Result = await self._session.execute(select(Comment).where(Comment.id == comment_id))
        if (comment := res.scalars().first()) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=DETAILERROR.NOT_FOUND.obj('Comment'))
        elif comment.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=DETAILERROR.CANNOT_DELETE.comment)
        await self._session.delete(comment)
        await self._session.commit()

    async def write_comment(self, article_id: int, text: str, user: User) -> Comment:
        res: Result = await self._session.execute(select(Article).where(Article.id == article_id))
        if not res.scalars().first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=DETAILERROR.NOT_FOUND.obj('Article'))
        comment_result: Result = await self._session.execute(
            insert(Comment).values(text=text, article_id=article_id, user_id=user.id).returning(Comment))
        await self._session.commit()
        return comment_result.first()

    async def get_all_comments_from_article(self, article_id: int) -> List[Comment]:
        article: Result = await self._session.execute(select(Article).where(Article.id == article_id))
        if not article.scalars().first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=DETAILERROR.NOT_FOUND.obj('Article'))
        res: Result = await self._session.execute(select(Comment).where(Comment.article_id == article_id))
        return res.scalars().all()
