from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional

from utils.roles import Role


class UserSchema(BaseModel):
    name: str
    login: str
    personal_info: str | None
    role: Role
    img_path: str | None

    model_config = ConfigDict(from_attributes=True)

class CourseSchema(BaseModel):
    name: str
    info: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class UserIdSchema(UserSchema):
    id: UUID

class CourseIdSchema(CourseSchema):
    id: UUID
    owner_id: UUID