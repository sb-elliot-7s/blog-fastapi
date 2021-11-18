from abc import ABC, abstractmethod
from typing import List
from comments.models import Comment
from auth.models import User


class CommentsRepositoryInterface(ABC):

    @abstractmethod
    async def write_comment(self, article_id: int, text: str, user: User) -> Comment: pass

    @abstractmethod
    async def delete_comment(self, comment_id: int, user: User) -> None: pass

    @abstractmethod
    async def get_all_comments_from_article(self, article_id: int) -> List[Comment]: pass
