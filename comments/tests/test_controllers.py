import pytest
from httpx import AsyncClient

from articles.models import Article
from endpoint import PrefixRoute


class TestCommentsController:

    @pytest.mark.parametrize('text, id_', [('first comment', 1), ('second comment', 2)])
    @pytest.mark.asyncio
    async def test_write_comment(self, first_client_with_jwt_token: AsyncClient, text: str, id_: int, first_article):
        res = await first_client_with_jwt_token.post(PrefixRoute.comments + f'/{first_article["id"]}', json={'text': text})
        assert res.status_code == 201
        assert res.json()['text'] == text
        assert 'id' in res.json()
        assert res.json()['id'] == id_

    @pytest.mark.asyncio
    async def test_write_comment_to_second_article(self, first_client_with_jwt_token: AsyncClient, second_article):
        data = {'text': 'python is the cool language'}
        res = await first_client_with_jwt_token.post(PrefixRoute.comments + f'/{second_article["id"]}', json=data)
        assert res.status_code == 201
        assert res.json()['text'] == 'python is the cool language'
        assert 'id' in res.json()
        assert res.json()['id'] == 3

    @pytest.mark.parametrize('article_id, status_code, number_of_comments', [(1, 200, 2), (2, 200, 1)])
    @pytest.mark.asyncio
    async def test_get_comments_for_article(self, client_without_jwt: AsyncClient, article_id: int, status_code: int,
                                            number_of_comments: int):
        res = await client_without_jwt.get(PrefixRoute.comments + f'/{article_id}')
        assert res.status_code == status_code
        assert len(res.json()) == number_of_comments

    @pytest.mark.asyncio
    async def test_failure_show_comments(self, first_client_with_jwt_token: AsyncClient):
        article_not_found = PrefixRoute.comments + '/7'
        res = await first_client_with_jwt_token.get(article_not_found)
        assert res.status_code == 404
        assert res.json()['detail'] == 'Article not found'

    @pytest.mark.asyncio
    async def test_delete_comment_by_second_user(self, second_client_with_jwt_token: AsyncClient):
        res = await second_client_with_jwt_token.delete(PrefixRoute.comments + '/1')
        assert res.json()['detail'] == 'You cannot delete this comment'
        assert res.status_code == 400

    @pytest.mark.parametrize('comment_id, status_code', [(1, 204), (2, 204), (3, 204), (4, 404)])
    @pytest.mark.asyncio
    async def test_delete_comment(self, first_client_with_jwt_token: AsyncClient, comment_id: int, status_code: int):
        res = await first_client_with_jwt_token.delete(PrefixRoute.comments + f'/{comment_id}')
        assert res.status_code == status_code

    @pytest.mark.parametrize('comment_id, status_code, key, value', [(1, 401, 'detail', 'Not authenticated')])
    @pytest.mark.asyncio
    async def test_failure_delete_comment(self, client_without_jwt: AsyncClient, comment_id: int, status_code: int, key: str,
                                          value: str):
        res = await client_without_jwt.delete(PrefixRoute.comments + f'/{comment_id}')
        assert res.status_code == status_code
        assert res.json()[key] == value

    @pytest.mark.asyncio
    async def test_write_comment_without_jwt(self, client_without_jwt: AsyncClient, second_article):
        data = {'text': 'hello world'}
        res = await client_without_jwt.post(PrefixRoute.comments + f'/{second_article["id"]}', json=data)
        assert res.status_code == 401
        assert res.json()['detail'] == 'Not authenticated'
