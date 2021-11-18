from pydantic import BaseModel
from datetime import datetime


class CommentCreateSchema(BaseModel):
    text: str


class CommentSchema(CommentCreateSchema):
    id: int
    article_id: int
    user_id: int
    created: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda d: d.strftime('%Y-%m-%d %H:%M:%S')
        }
