from auth.models import User
from auth.token_service import TokenService
from permissions import GetUser
from database import get_db
from fastapi import APIRouter, Depends, status
from .schemas import CommentCreateSchema, CommentSchema
from sqlalchemy.ext.asyncio import AsyncSession
from .services import CommentsService
from .repository import CommentRepository
from endpoint import Endpoint, TagsRoute, PrefixRoute

comments_router = APIRouter(tags=[TagsRoute.comments], prefix=PrefixRoute.comments)


@comments_router.get(Endpoint.comment_from_article_id_, response_model=list[CommentSchema], status_code=status.HTTP_200_OK)
async def all_comments_for_article(article_id: int, db: AsyncSession = Depends(get_db)):
    return await CommentsService(repository=CommentRepository(session=db)).get_all_comments_from_article(article_id=article_id)


@comments_router.post(Endpoint.write_comment_for_article, response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
async def write_comment(article_id: int, comment: CommentCreateSchema, db: AsyncSession = Depends(get_db),
                        user: User = Depends(GetUser(TokenService()))):
    return await CommentsService(repository=CommentRepository(session=db)) \
        .write_comment(text=comment.text, article_id=article_id, user=user)


@comments_router.delete(Endpoint.delete_comment, status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(GetUser(TokenService()))):
    return await CommentsService(repository=CommentRepository(session=db)).delete_comment(comment_id=comment_id, user=user)
