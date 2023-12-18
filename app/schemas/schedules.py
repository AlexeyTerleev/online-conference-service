from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, validator
from schemas.base import CourseIdSchema


class ScheduleSchema(BaseModel):
    start_date_time: datetime
    end_date_time: datetime

    model_config = ConfigDict(from_attributes=True)

    @validator('end_date_time')
    def validate_end_date(cls, end_date, values):
        if 'start_date_time' in values and end_date < values['start_date_time']:
            raise ValueError("End date must be after the start date")
        return end_date


class ScheduleRegisterSchema(ScheduleSchema):
    ...


class ScheduleCreateSchema(ScheduleSchema):
    course_id: UUID
    room_id: Optional[UUID] = None


class ScheduleOutSchema(ScheduleSchema):
    id: UUID
    course: CourseIdSchema
    room_id: Optional[UUID] = None