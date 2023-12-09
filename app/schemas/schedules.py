from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, validator


class ScheduleSchema(BaseModel):
    start_date_time: datetime
    end_date_time: datetime

    model_config = ConfigDict(from_attributes=True)

    @validator('end_date_time', pre=True, always=True)
    def validate_password(cls, value, values):
        if values.get('start_date_time') > value:
            raise ValueError("Start time should be less then end time")
        return value


class ScheduleRegisterSchema(ScheduleSchema):
    ...


class ScheduleCreateSchema(ScheduleSchema):
    course_id: UUID
    room_id: Optional[UUID] = None


class ScheduleOutSchema(ScheduleSchema):
    id: UUID
    course_id: UUID
    room_id: Optional[UUID] = None