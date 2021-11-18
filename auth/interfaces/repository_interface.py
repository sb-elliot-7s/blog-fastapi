from abc import ABC, abstractmethod
from auth.models import User
from ..schemas import UserUpdateSchema


class AuthUserRepositoryInterface(ABC):

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User: pass

    @abstractmethod
    async def save_user(self, email: str, username: str, password: str): pass


class UserInterface(ABC):

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User: pass

    @abstractmethod
    async def update_user(self, data: UserUpdateSchema, user: User) -> User: pass

    @abstractmethod
    async def delete_user(self, user: User): pass
