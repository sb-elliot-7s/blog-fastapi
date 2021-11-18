from typing import Optional

from sqlalchemy.engine import Result
from .models import User
from sqlalchemy.ext.asyncio import AsyncSession
from .interfaces.repository_interface import AuthUserRepositoryInterface, UserInterface
from sqlalchemy import select, insert, update
from fastapi import HTTPException, status
from message_error import DETAILERROR
from .schemas import UserUpdateSchema


class AuthUserRepository(AuthUserRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_email(self, email: str) -> User:
        res: Result = await self._session.execute(select(User).filter_by(email=email))
        return res.scalars().first()

    async def save_user(self, email: str, username: str, password: str):
        res: Result = await self._session.execute(
            insert(User).values(email=email, username=username, password=password).returning(User))
        await self._session.commit()
        return res.first()


class UserRepository(UserInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_id(self, user_id: int) -> User:
        res: Result = await self._session.execute(select(User).where(User.id == user_id))
        if not (user := res.scalars().first()):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=DETAILERROR.NOT_FOUND.obj('User'))
        return user

    async def update_user(self, data: UserUpdateSchema, user: User):
        _user = await self.get_user_by_id(user_id=user.id)
        _ = await self._session.execute(
            update(User).where(User.id == _user.id).values(**data.dict(exclude_none=True)).returning(User))
        await self._session.commit()
        await self._session.refresh(_user)
        return _user

    async def delete_user(self, user: User):
        _user = await self.get_user_by_id(user_id=user.id)
        await self._session.delete(_user)
        await self._session.commit()
        return True
