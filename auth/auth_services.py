from .models import User
from .interfaces.token_interface import TokenInterface
from .interfaces.password_interface import PasswordSecurityInterface
from .interfaces.repository_interface import AuthUserRepositoryInterface
from typing import Optional
from settings_config import get_settings
from fastapi import status, HTTPException
from .schemas import Token

from message_error import DETAILERROR


class AuthService:

    def __init__(self, password_security_service: PasswordSecurityInterface, repository: AuthUserRepositoryInterface):
        self._password_security_service = password_security_service
        self._repository = repository
        self._settings = get_settings()

    async def _authenticate(self, email: str, password: str):
        if not (user := await self._repository.get_user_by_email(email=email)) \
                or not await self._password_security_service.verify_password(plain_password=password,
                                                                             hashed_password=user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=DETAILERROR.INCORRECT_EMAIL_OR_PASSWORD)
        return user

    async def sign_up(self, email: str, password: str, username: Optional[str]) -> User:
        if await self._repository.get_user_by_email(email=email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=DETAILERROR.USER_WITH_THIS_EMAIL_EXISTS)
        hashed_password = await self._password_security_service.get_password_hash(password)
        return await self._repository.save_user(email=email, username=username, password=hashed_password)

    async def login(self, email: str, password: str, token_service: TokenInterface) -> Token:
        user = await self._authenticate(email, password)
        subject = {'sub': user.email}
        access_token: str = await token_service \
            .create_token_for_user(data=subject, secret_key=self._settings.secret_key,
                                   exp_time=self._settings.access_token_expire_minutes,
                                   algorithm=self._settings.algorithm)
        return Token(access_token=access_token, token_type='bearer')
