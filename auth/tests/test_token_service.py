import pytest
from jose import JWSError

from auth.token_service import TokenService
from settings_config import get_settings
from fastapi import HTTPException
from datetime import datetime, timedelta


class TestTokenService:

    @pytest.mark.parametrize('email, exp_time', [('test@test.com', 15), ('test@test.com', 30)])
    @pytest.mark.asyncio
    async def test_successfully_create_access_token(self, get_token_service: TokenService, email: str, exp_time: int):
        access_token = await get_token_service. \
            create_token_for_user(data={'sub': email}, secret_key=get_settings().secret_key, exp_time=exp_time,
                                  algorithm=get_settings().algorithm)
        assert len(access_token.split('.')) == 3  # ['dfk...', '24a3s2sj...', '..324ljl']
        data = await get_token_service. \
            verify_token(token=access_token, key=get_settings().secret_key, algorithm=get_settings().algorithm)
        # expected data = {'sub': 'test@test.com','exp': 1636561789}
        assert data.get('sub') is not None
        token_exp_time = datetime.fromtimestamp(int(data['exp'])).strftime('%Y-%m-%d %H:%M')
        time_now = datetime.now()
        delta = timedelta(minutes=exp_time)
        expected_time = (time_now + delta).strftime('%Y-%m-%d %H:%M')
        assert token_exp_time == expected_time
        assert data['sub'] == email

    @pytest.mark.asyncio
    async def test_failure_decode_token(self, get_token_service):
        wrong_token = 'I1NiIsInR5cCI7777776IkpXVaCJ9.JleHAiOj1111111E2MzY1NjQ3MDV9.JleHAiOjE2MzY1NjQ3MDV9'
        with pytest.raises(HTTPException):
            _ = await get_token_service.verify_token(token=wrong_token, key=get_settings().secret_key,
                                                     algorithm=get_settings().algorithm)

    @pytest.mark.parametrize('data, secret_key, algorithm, expected_error', [
        ({'sub': 'test@test.com'}, None, get_settings().algorithm, JWSError),
        ({'sub': 'test@test.com'}, get_settings().secret_key, None, JWSError),
        ('str', get_settings().secret_key, get_settings().algorithm, AttributeError),
        (None, get_settings().secret_key, get_settings().algorithm, AttributeError),
    ])
    @pytest.mark.asyncio
    async def test_invalid_create_access_token_raises_error(self, get_token_service, data, secret_key, algorithm, expected_error):
        with pytest.raises(expected_error):
            _ = await get_token_service.create_token_for_user(data=data, secret_key=secret_key,
                                                              exp_time=get_settings().access_token_expire_minutes,
                                                              algorithm=algorithm)
