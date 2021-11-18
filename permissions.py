from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from auth.interfaces.token_interface import TokenInterface
from database import get_db
from settings_config import get_settings
from fastapi.security import OAuth2PasswordBearer
from auth.models import User
from fastapi import Depends


class GetUser:
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='auth/login')

    def __init__(self, token_service: TokenInterface):
        self._token_service = token_service

    async def __call__(self, db: AsyncSession = Depends(get_db), token: str = Depends(OAUTH2_SCHEME)):
        payload = await self._token_service \
            .verify_token(token=token, key=get_settings().secret_key, algorithm=get_settings().algorithm)
        email = payload.get('sub', None)  # {'sub': 'example@gmail.com', 'exp': '16363.....'}.get('sub')
        res: Result = await db.execute(select(User).where(User.email == email, User.is_active))
        return res.scalars().first()
