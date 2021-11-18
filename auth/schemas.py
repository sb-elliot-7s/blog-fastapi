from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    email: EmailStr
    username: Optional[str] = Field(None, max_length=255)


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=10)


class UserUpdateSchema(BaseModel):
    bio: Optional[str] = Field(None, max_length=255)
    username: Optional[str] = Field(None, max_length=255)


class UserSchema(UserBaseSchema):
    id: int
    bio: Optional[str] = Field(None, max_length=255)
    is_active: bool = True
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda d: d.strftime('%Y-%m-%d %H:%M:%S')
        }
        schema_extra = {
            'example': {
                "email": "example@gmail.com",
                "username": "exampleName",
                "id": 1,
                "bio": 'some bio',
                "is_active": True,
                "created": "2021-10-14T16:02:51.250784",
                "updated": "2021-10-14T16:02:51.250799"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str
