import pytest
from httpx import AsyncClient
from endpoint import PrefixRoute, Endpoint


async def save_article(client: AsyncClient, title: str, content: str):
    HEADERS = {'content-type': 'application/x-www-form-urlencoded'}
    res = await client.post(PrefixRoute.articles + Endpoint.slash, data={'title': title, 'content': content}, headers=HEADERS)
    return res.json()


@pytest.fixture(scope='module')
async def first_article(first_client_with_jwt_token: AsyncClient):
    return await save_article(client=first_client_with_jwt_token, title='first title', content='first content')


@pytest.fixture(scope='module')
async def second_article(first_client_with_jwt_token: AsyncClient):
    return await save_article(client=first_client_with_jwt_token, title='second title', content='second content')
