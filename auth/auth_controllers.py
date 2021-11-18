from fastapi.responses import JSONResponse
from .token_service import TokenService
from passlib.context import CryptContext
from .password_security_service import PasswordSecurity
from .auth_services import AuthService
from .schemas import UserCreateSchema, Token, UserSchema
from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from .repostitory import AuthUserRepository
from database import get_db
from endpoint import Endpoint, TagsRoute, PrefixRoute

auth_router = APIRouter(tags=[TagsRoute.auth], prefix=PrefixRoute.auth)


@auth_router.post(Endpoint.signup, response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def sign_up(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    return await AuthService(
        password_security_service=PasswordSecurity(context=CryptContext(schemes=["bcrypt"], deprecated="auto")),
        repository=AuthUserRepository(session=db)
    ).sign_up(**user.dict())


@auth_router.post(Endpoint.login, response_model=Token, status_code=status.HTTP_200_OK)
async def login(email: str = Form(...), password: str = Form(..., min_lenght=10), db: AsyncSession = Depends(get_db)):
    token_data = await AuthService(
        password_security_service=PasswordSecurity(context=CryptContext(schemes=["bcrypt"], deprecated="auto")),
        repository=AuthUserRepository(session=db)
    ).login(email=email, password=password, token_service=TokenService())
    response = JSONResponse(token_data.dict())
    response.set_cookie(key='access_token', value=token_data.access_token, httponly=True)
    return response
