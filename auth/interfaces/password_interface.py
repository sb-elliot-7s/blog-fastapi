from abc import ABC, abstractmethod


class PasswordSecurityInterface(ABC):

    @abstractmethod
    async def get_password_hash(self, password: str) -> str: pass

    @abstractmethod
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool: pass
