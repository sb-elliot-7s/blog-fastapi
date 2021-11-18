from .interfaces.repository_interface import UserInterface
from .models import User
from .schemas import UserUpdateSchema
from fastapi.responses import Response
from fastapi import status


class UserService:

    def __init__(self, repository: UserInterface):
        self._repository = repository

    async def update_user(self, data: UserUpdateSchema, user: User):
        return await self._repository.update_user(data=data, user=user)

    async def delete_user(self, user: User):
        await self._repository.delete_user(user=user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def get_user_by_id(self, user_id: int):
        return await self._repository.get_user_by_id(user_id=user_id)
