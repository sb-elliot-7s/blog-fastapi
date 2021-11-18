import pytest
from httpx import AsyncClient
from endpoint import PrefixRoute, Endpoint


class TestUser:
    HEADERS = {'content-type': 'application/x-www-form-urlencoded'}

    @pytest.mark.parametrize('user_id, status_code, key, value', [
        (1, 200, 'email', 'first_user@example.com',),
        (2, 404, 'detail', 'User not found')
    ])
    @pytest.mark.asyncio
    async def test_get_user_by_id_or_not_found(self, first_client_with_jwt_token: AsyncClient, user_id: int, status_code: int,
                                               key: str, value: str):
        res = await first_client_with_jwt_token.get(PrefixRoute.user + f'/{user_id}')
        assert res.status_code == status_code
        assert res.json()[key] == value

    @pytest.mark.parametrize('bio, username, email, id_', [
        ('new bio', 'kali_linux', 'first_user@example.com', 1),
        ('about me', 'macos', 'first_user@example.com', 1),
    ])
    @pytest.mark.asyncio
    async def test_update_user(self, first_client_with_jwt_token: AsyncClient, bio: str, username: str, id_: int, email: str):
        data = {'bio': bio, 'username': username}
        res = await first_client_with_jwt_token.put(PrefixRoute.user + Endpoint.slash, json=data)
        assert res.status_code == 200
        assert res.json()['id'] == id_
        assert res.json()['email'] == email
        assert res.json()['bio'] == bio
        assert res.json()['username'] == username

    @pytest.mark.asyncio
    async def test_delete_user(self, first_client_with_jwt_token: AsyncClient):
        res = await first_client_with_jwt_token.delete(PrefixRoute.user + Endpoint.slash)
        assert res.status_code == 204
