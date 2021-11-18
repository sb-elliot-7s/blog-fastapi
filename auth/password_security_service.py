from .interfaces.password_interface import PasswordSecurityInterface
from passlib.context import CryptContext


class PasswordSecurity(PasswordSecurityInterface):

    def __init__(self, context: CryptContext):
        self._context = context

    async def get_password_hash(self, password: str) -> str:
        return self._context.hash(password)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._context.verify(plain_password, hashed_password)
