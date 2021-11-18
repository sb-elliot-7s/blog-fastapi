from typing import Optional
import aiofiles
import pytest
from httpx import AsyncClient
from endpoint import Endpoint, PrefixRoute
from message_error import DETAILERROR
from settings_config import get_settings
from collections import namedtuple


class TestArticle:
    """
    -- retrieve all articles => retrieve empty list => 200 -> []
    -- write 3 articles (with one image, two images and without images) => list of 3 articles => 201
    -- retrieve image and delete => 204
    -- write article without access_token => 401 unauthorized
    -- retrieve articles => length 3
    -- write article : title > 255 letters, empty title or empty content => 422
    -- retrieve user articles => length 3 => 200
    -- article by id => 200 if article exists else 404
    -- update article => 200 if article exists else 404
    -- delete article by id => del id 1, id 2, id 3 => 204; id 4 does not exist => 404
    -- retrieve all articles => empty list => 200
    -- delete, update by second user => 400, not update, not delete
    """

    WriteArticle = namedtuple('ArticleTest', 'title content list_images count_of_images')

    first_article = WriteArticle(title='first article with one image', content='first content',
                                 list_images=[get_settings().test_image_path], count_of_images=1)
    second_article = WriteArticle(title='second article with two images', content='second content',
                                  list_images=[get_settings().test_image_path, get_settings().test_image_path],
                                  count_of_images=2)
    third_article = WriteArticle(title='third article without images', content='third content', list_images=None,
                                 count_of_images=0)

    HEADERS = {'content-type': 'application/x-www-form-urlencoded'}
    COMMON_DATA = {'title': 'common title', 'content': 'common content'}
    MORE_THAN_255_LETTERS = 'Django is a python based open-source framework for building web applications. ' \
                            'It was developed by Adrian Holovaty and Simon Willison at Django Software ' \
                            'Foundation was first released in 2005. Django is widely used today and is ' \
                            'rapidly growing. Django is popular for it’s rapid pace for building web apps.'

    @pytest.mark.asyncio
    async def test_empty_articles(self, client_without_jwt: AsyncClient):
        res = await client_without_jwt.get(PrefixRoute.articles + Endpoint.slash)
        assert res.status_code == 200
        assert not len(res.json())

    @pytest.mark.parametrize('title, content, list_images, count_of_images, saved_article_id',
                             [(*first_article, 1), (*second_article, 2), (*third_article, 3)])
    @pytest.mark.asyncio
    async def test_write_article(self, first_client_with_jwt_token: AsyncClient, title: str, content: str,
                                 saved_article_id: int, list_images: Optional[list[str]], count_of_images: int):
        files = []
        if list_images:
            for image in list_images:
                async with aiofiles.open(image, mode='rb') as f:
                    t = ('files', (image.split('/')[-1], await f.read()))
                    files.append(t)
        res = await first_client_with_jwt_token.post(PrefixRoute.articles + Endpoint.slash,
                                                     data={'title': title, 'content': content},
                                                     files=files if list_images else None)
        assert res.status_code == 201
        assert res.json()['id'] == saved_article_id
        assert res.json()['title'] == title
        assert res.json()['content'] == content
        assert len(res.json()['images']) == count_of_images

    @pytest.mark.parametrize('article_id, method, status_code', [(1, 'GET', 200), (1, 'DELETE', 204), (2, 'DELETE', 204)])
    @pytest.mark.asyncio
    async def test_image_get_and_delete(self, first_client_with_jwt_token: AsyncClient, method: str, status_code: int,
                                        article_id: int):
        article = await first_client_with_jwt_token.get(PrefixRoute.articles + f'/{article_id}')
        # {'title': 'xx', ..., 'images': [{'photo': 'http://127.0.0.1:8000/articles/images/sj...1r:win11.jpeg', 'article_id: 1'}]}
        images: list[dict] = article.json()['images']
        for img in images:
            photo = img.get('photo').split('/')[-1]
            request = first_client_with_jwt_token.build_request(method=method, url=PrefixRoute.articles + f'/images/{photo}')
            response = await first_client_with_jwt_token.send(request)
            assert response.status_code == status_code

    @pytest.mark.asyncio
    async def test_write_article_without_jwt(self, client_without_jwt: AsyncClient):
        res = await client_without_jwt.post(PrefixRoute.articles + Endpoint.slash, data=self.COMMON_DATA)
        assert res.status_code == 401
        assert res.json()['detail'] == 'Not authenticated'

    @pytest.mark.parametrize('title, content, status_code, detail',
                             [(MORE_THAN_255_LETTERS, 'content', 422, 'ensure this value has at most 255 characters'),
                              ('title', None, 422, 'field required'), (None, 'content', 422, 'field required')])
    @pytest.mark.asyncio
    async def test_failure_write_article(self, first_client_with_jwt_token: AsyncClient, title: str, content: str,
                                         status_code: str, detail: str):
        data = {'title': title, 'content': content}
        res = await first_client_with_jwt_token.post(PrefixRoute.articles + Endpoint.slash, data=data)
        assert res.status_code == status_code
        assert res.json()['detail'][0].get('msg') == detail

    @pytest.mark.asyncio
    async def test_get_all_articles(self, client_without_jwt: AsyncClient):
        res = await client_without_jwt.get(PrefixRoute.articles + Endpoint.slash)
        assert res.status_code == 200
        assert len(res.json()) == 3

    @pytest.mark.asyncio
    async def test_get_user_articles(self, client_without_jwt: AsyncClient):
        res = await client_without_jwt.get(PrefixRoute.articles + '/user/1')
        assert res.status_code == 200
        assert len(res.json()) == 3
        assert res.json()[0]['user_id'] == 1

    @pytest.mark.asyncio
    async def test_get_user_articles_if_user_not_found(self, client_without_jwt: AsyncClient):
        res = await client_without_jwt.get(PrefixRoute.articles + '/user/77')
        assert res.status_code == 404
        assert res.json()['detail'] == DETAILERROR.NOT_FOUND.obj('User')

    @pytest.mark.parametrize('article_id, status_code, key, value',
                             [(1, 200, 'title', first_article.title), (2, 200, 'title', second_article.title),
                              (3, 200, 'title', third_article.title),
                              (4, 404, 'detail', DETAILERROR.NOT_FOUND.obj('Article'))])
    @pytest.mark.asyncio
    async def test_get_article_or_not_found(self, client_without_jwt: AsyncClient, article_id: int, status_code: int, key: str,
                                            value: str):
        res = await client_without_jwt.get(PrefixRoute.articles + f'/{article_id}')
        assert res.status_code == status_code
        assert res.json()[key] == value

    @pytest.mark.asyncio
    async def test_update_article_by_second_user(self, second_client_with_jwt_token: AsyncClient):
        res = await second_client_with_jwt_token.put(PrefixRoute.articles + '/1', data=self.COMMON_DATA, headers=self.HEADERS)
        assert res.status_code == 400
        assert res.json()['detail'] == DETAILERROR.CANNOT_UPDATE.article

    @pytest.mark.parametrize('article_id, title, content, status_code, key, value', [
        (1, 'updated title', 'updated content', 200, 'title', 'updated title'),
        (4, 'x', 'x', 404, 'detail', DETAILERROR.NOT_FOUND.obj('Article'))])
    @pytest.mark.asyncio
    async def test_update_article(self, first_client_with_jwt_token: AsyncClient, article_id: int, status_code: int, title: str,
                                  content: str, key: str, value: str):
        data = {'title': title, 'content': content}
        res = await first_client_with_jwt_token.put(PrefixRoute.articles + f'/{article_id}', data=data, headers=self.HEADERS)
        assert res.status_code == status_code
        assert res.json()[key] == value

    @pytest.mark.asyncio
    async def test_delete_article_by_second_user(self, second_client_with_jwt_token: AsyncClient):
        res = await second_client_with_jwt_token.delete(PrefixRoute.articles + '/1')
        assert res.json()['detail'] == DETAILERROR.CANNOT_DELETE.article
        assert res.status_code == 400

    @pytest.mark.parametrize('article_id, status_code', [(1, 204), (2, 204), (3, 204), (4, 404)])
    @pytest.mark.asyncio
    async def test_delete_article_or_not_found(self, first_client_with_jwt_token: AsyncClient, article_id: int, status_code: int):
        res = await first_client_with_jwt_token.delete(PrefixRoute.articles + f'/{article_id}')
        assert res.status_code == status_code

    @pytest.mark.asyncio
    async def test_get_all_articles(self, client_without_jwt: AsyncClient):
        res = await client_without_jwt.get(PrefixRoute.articles + Endpoint.slash)
        assert res.status_code == 200
        assert not len(res.json())
