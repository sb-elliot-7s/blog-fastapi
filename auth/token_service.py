from message_error import DETAILERROR
from .interfaces.token_interface import TokenInterface
from datetime import timedelta, datetime
from typing import Optional
from fastapi import status, HTTPException
from jose import jwt, JWTError


class TokenService(TokenInterface):

    async def create_token_for_user(self, data: dict, secret_key: str, exp_time: Optional[int], algorithm: str) -> str:
        payload = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=exp_time) if exp_time else datetime.utcnow() + timedelta(minutes=15)
        payload.update({'exp': expire})
        token = jwt.encode(claims=payload, key=secret_key, algorithm=algorithm)
        return token

    async def verify_token(self, token: str, key: str, algorithm: str) -> dict:
        try:
            payload = jwt.decode(token=token, key=key, algorithms=algorithm)
        except (JWTError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=DETAILERROR.NOT_VALIDATE_CREDENTIALS, headers={"WWW-Authenticate": "Bearer"})
        return payload
