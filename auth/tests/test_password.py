import pytest
from auth.password_security_service import PasswordSecurity
from passlib.context import CryptContext


class TestPasswordService:

    @pytest.fixture
    def get_password_security(self):
        return PasswordSecurity(context=CryptContext(schemes=['bcrypt'], deprecated='auto'))

    @pytest.mark.parametrize('password', ['1234567890', 'test123'])
    @pytest.mark.asyncio
    async def test_successfully_verify_passwords(self, password, get_password_security):
        hashed_password = await get_password_security.get_password_hash(password=password)
        assert len(hashed_password)
        assert await get_password_security.verify_password(plain_password=password, hashed_password=hashed_password)
