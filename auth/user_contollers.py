from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from endpoint import PrefixRoute, Endpoint, TagsRoute
from permissions import GetUser
from .models import User
from .repostitory import UserRepository
from .schemas import UserUpdateSchema, UserSchema
from .token_service import TokenService
from .user_services import UserService

user_router = APIRouter(tags=[TagsRoute.user], prefix=PrefixRoute.user)


@user_router.delete(Endpoint.slash, status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: AsyncSession = Depends(get_db), user: User = Depends(GetUser(token_service=TokenService()))):
    return await UserService(repository=UserRepository(session=db)).delete_user(user=user)


@user_router.put(Endpoint.slash, response_model=UserSchema, status_code=status.HTTP_200_OK)
async def update_user(updated_data: UserUpdateSchema, db: AsyncSession = Depends(get_db),
                      user: User = Depends(GetUser(token_service=TokenService()))):
    return await UserService(repository=UserRepository(session=db)).update_user(data=updated_data, user=user)


@user_router.get(Endpoint.user_id, status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService(repository=UserRepository(session=db)).get_user_by_id(user_id=user_id)
