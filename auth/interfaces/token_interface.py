from abc import ABC, abstractmethod
from typing import Optional


class TokenInterface(ABC):

    @abstractmethod
    async def create_token_for_user(self, data: dict, secret_key: str, exp_time: Optional[int], algorithm: str) -> str: pass

    @abstractmethod
    async def verify_token(self, token: str, key: str, algorithm: str) -> dict: pass
