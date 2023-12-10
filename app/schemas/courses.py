from typing import List
from uuid import UUID

from schemas.base import CourseSchema, CourseIdSchema, UserIdSchema
from schemas.schedules import ScheduleRegisterSchema

class CourseRegisterSchema(CourseSchema):
    schedules: List[ScheduleRegisterSchema]


class CourseCreateSchema(CourseSchema):
    ...


class CourseDbSchema(CourseIdSchema):
    ...


class CourseOutSchema(CourseIdSchema):
    users: List[UserIdSchema]