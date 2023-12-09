from typing import List
from pydantic import BaseModel, HttpUrl

from utils.roles import Role
from schemas.base import UserSchema, UserIdSchema, CourseIdSchema


class UserRegisterSchema(UserSchema):
    password: str
    img_path: HttpUrl | None = None


class UserCreateSchema(UserSchema):
    hashed_password: str


class UserUpdateSchema(BaseModel):
    name: str | None
    login: str | None
    personal_info: str | None
    role: Role | None
    img_path: HttpUrl | None


class UserUpgradeSchema(BaseModel):
    name: str | None
    login: str | None
    personal_info: str | None
    role: Role | None
    img_path: HttpUrl | None


class UserDbSchema(UserIdSchema):
    hashed_password: str


class UserOutSchema(UserIdSchema):
    courses: List[CourseIdSchema]

