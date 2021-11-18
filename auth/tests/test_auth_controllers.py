import pytest
from httpx import AsyncClient

from endpoint import Endpoint, PrefixRoute
from message_error import DETAILERROR
from collections import namedtuple


class TestAuth:
    EMAIL_FIELD_REQUIRED = [{'loc': ['body', 'email'], 'msg': 'field required', 'type': 'value_error.missing'}]
    PASSWORD_FIELD_REQUIRED = [{'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}]
    LESS_THAN_10_CHARACTERS_IN_PASSWORD = [{'loc': ['body', 'password'], 'msg': 'ensure this value has at least 10 characters',
                                            'type': 'value_error.any_str.min_length', 'ctx': {'limit_value': 10}}]
    SIGN_UP_URL = PrefixRoute.auth + Endpoint.signup
    LOGIN_URL = PrefixRoute.auth + Endpoint.login
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

    SignUpUser = namedtuple('SignUpUser', 'username, password, email')
    a_user = SignUpUser(username='a_user', password='1234567890', email='a@gmail.com')
    b_user = SignUpUser(username=None, password='1234567890', email='b@gmail.com')

    @pytest.mark.parametrize('username, password, email, response', [
        (*a_user, {"email": a_user.email, "username": a_user.username, "is_active": True}),
        (*b_user, {"email": b_user.email, "username": b_user.username, "is_active": True})
    ])
    @pytest.mark.asyncio
    async def test_signup(self, client_without_jwt: AsyncClient, username: str, password: str, email: str, response: dict):
        res = await client_without_jwt.post(self.SIGN_UP_URL, json={'username': username, 'password': password, 'email': email})
        assert res.status_code == 201
        assert res.json()['is_active'] == response['is_active']
        assert res.json()['email'] == response['email']
        assert 'password' not in res.json()

    @pytest.mark.parametrize('email, password, status_code, key, value', [
        ('hello@hello.com', '123456789', 422, 'detail', LESS_THAN_10_CHARACTERS_IN_PASSWORD),
        (a_user.email, a_user.password, 400, 'detail', DETAILERROR.USER_WITH_THIS_EMAIL_EXISTS)
    ])
    @pytest.mark.asyncio
    async def test_failure_signup(self, client_without_jwt: AsyncClient, email: str, password: str, status_code: int, key: str,
                                  value: str):
        res = await client_without_jwt.post(self.SIGN_UP_URL, json={'email': email, 'password': password})
        assert res.status_code == status_code
        assert res.json()[key] == value

    @pytest.mark.parametrize('email, password, status',
                             [(a_user.email, a_user.password, 200), (b_user.email, b_user.password, 200)])
    @pytest.mark.asyncio
    async def test_successfully_login(self, client_without_jwt: AsyncClient, email: str, password: str, status: int):
        res = await client_without_jwt.post(self.LOGIN_URL, data={'email': email, 'password': password}, headers=self.HEADERS)
        assert res.status_code == status
        assert 'access_token' in res.json()

    @pytest.mark.parametrize('email, password, status_code, key, value', [
        ('a@test.com', 'wrong-password', 400, 'detail', DETAILERROR.INCORRECT_EMAIL_OR_PASSWORD),
        ('wrong@gmail.com', '1234567890', 400, 'detail', DETAILERROR.INCORRECT_EMAIL_OR_PASSWORD),
        (None, '1234567890', 422, 'detail', EMAIL_FIELD_REQUIRED),
        ('a@test.com', None, 422, 'detail', PASSWORD_FIELD_REQUIRED),
    ])
    @pytest.mark.asyncio
    async def test_failure_login(self, client_without_jwt: AsyncClient, email: str, password: str, status_code: int, key: str,
                                 value: str):
        res = await client_without_jwt.post(self.LOGIN_URL, data={'email': email, 'password': password}, headers=self.HEADERS)
        assert res.status_code == status_code
        assert res.json()[key] == value
        assert 'access_token' not in res.json()
