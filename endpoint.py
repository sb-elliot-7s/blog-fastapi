from enum import Enum


class Endpoint(str, Enum):
    slash = '/'

    comment_from_article_id_ = '/{article_id}'
    write_comment_for_article = '/{article_id}'
    delete_comment = '/{comment_id}'

    user_articles = '/user/{user_id}'
    single_article = "/{article_id}"
    image = '/images/{filename}'

    login = '/login'
    signup = '/signup'

    user_id = '/{user_id}'


class TagsRoute(str, Enum):
    articles = 'articles'
    comments = 'comments'
    auth = 'auth'
    user = 'user'


class PrefixRoute(str, Enum):
    articles = '/articles'
    comments = '/comments'
    auth = '/auth'
    user = '/user'
