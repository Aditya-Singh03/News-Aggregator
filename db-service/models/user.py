import re
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, Field, field_validator


class Token(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    token: str

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "sample",
                "token": "sample",
            }
        }


class UserVotes(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str

    list_of_posts_upvotes: List[str] = []
    list_of_posts_downvotes: List[str] = []

    list_of_comments_upvotes: List[str] = []
    list_of_comments_downvotes: List[str] = []

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "sample",
                "list_of_posts_upvotes": ["sample"],
                "list_of_posts_downvotes": ["sample"],
                "list_of_comments_upvotes": ["sample"],
                "list_of_comments_downvotes": ["sample"],
            }
        }


def check_pwd(pwd):
    re_for_pwd: re.Pattern[str] = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$")
    if not re_for_pwd.match(pwd):
        raise ValueError(
            "Invalid password - must contain at least 1 letter and 1 number and"
            "be at least 5 characters long"
        )
    return pwd


class UpdateUser(BaseModel):
    email_address: EmailStr = None
    password: str = None
    username: str = None
    avatar: int = None

    @field_validator("password")
    @classmethod
    def regex_match(cls, pwd: str) -> str:
        return check_pwd(pwd)


class RegisterUser(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    email_address: EmailStr
    password: str
    username: str
    avatar: int

    @field_validator("password")
    @classmethod
    def regex_match(cls, pwd: str) -> str:
        return check_pwd(pwd)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "email_address": "john_doe@gmail.com",
                "password": "password",
                "username": "john_doe",
                "avatar": 1,
            }
        }


class LoginUser(BaseModel):
    email_address: EmailStr
    password: str

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "email_address": "john_doe@gmail.com",
                "password": "password",
            }
        }


class Preferences(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    preferences: List[str]

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "preferences": ["sports", "food", "mastering the art of getting bored"]
            }
        }
