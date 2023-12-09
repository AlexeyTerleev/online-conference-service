from uuid import UUID
from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)


class UserIdSchema(UserSchema):
    id: UUID

class CourseIdSchema(CourseSchema):
    id: UUID