from datetime import datetime
from typing import List, Optional, Union

from fastapi import FastAPI
from typing import Union
import bcrypt
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from pydantic import EmailStr
import uuid


class User(BaseModel):
    id: Union[int, None] = None
    name: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None

    class config:
        orm_mode = True

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "name": "Billy",
    #                 "email": "Apple@gmail.com",
    #                 "password": "password",
    #             }
    #         ]
    #     }
    # }


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    email: Union[str, None] = None
    password: Union[str, None] = None

    class config:
        orm_mode = True

    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "email": "Apple@gmail.com",
    #                 "password": "password",
    #             }
    #         ]
    #     }
    # }


class BlogImageBase(BaseModel):
    id: int
    blog_post_id: int
    image_url: str

    class Config:
        orm_mode = True

class BlogPostBase(BaseModel):
    id: int
    title: str
    content: str
    category: str
    author: str
    created_at: Union[datetime, None] = None
    images: List[BlogImageBase] = []

    class Config:
        orm_mode = True