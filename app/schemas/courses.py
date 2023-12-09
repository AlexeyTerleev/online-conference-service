from typing import List
from uuid import UUID

from schemas.base import CourseSchema, CourseIdSchema, UserIdSchema


class CourseRegisterSchema(CourseSchema):
    ...


class CourseCreateSchema(CourseSchema):
    ...


class CourseDbSchema(CourseIdSchema):
    ...


class CourseOutSchema(CourseIdSchema):
    users: List[UserIdSchema]