from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from comments.schemas import CommentSchema


class ImageBaseSchema(BaseModel):
    photo: Optional[str]


class ImageSchema(ImageBaseSchema):
    id: int
    article_id: int

    class Config:
        orm_mode = True


class ArticleBaseSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = Field(None)


class ArticleCreateSchema(ArticleBaseSchema):
    pass


class CreatedArticleSchema(ArticleBaseSchema):
    id: int
    user_id: int
    created: datetime
    images: List[ImageSchema] = []

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda d: d.strftime('%Y-%m-%d %H:%M:%S')
        }


class ArticleSchema(CreatedArticleSchema):
    updated: datetime
    comments: List[CommentSchema] = []

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda d: d.strftime('%Y-%m-%d %H:%M:%S')
        }
        schema_extra = {
            'example': {
                'id': 1,
                'title': 'Hello, friend',
                'content': 'hello friend',
                'user_id': 1,
                'created': '2032-04-23T10:20:30.400+02:30',
                'updated': '2032-04-23T10:20:30.400+02:30',
                'is_active': True,
                'comments': [],
                'images': []
            }
        }
