from db.db import Base
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4

from schemas.schedules import ScheduleOutSchema


class Schedules(Base):
    __tablename__ = "schedules"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    start_date_time: Mapped[datetime]
    end_date_time: Mapped[datetime]
    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"))
    room_id: Mapped[UUID] = mapped_column(ForeignKey("rooms.id"))

    def to_read_model(self) -> ScheduleOutSchema:
        return ScheduleOutSchema(
            id=self.id,
            start_date_time=self.start_date_time,
            pasend_date_timesword=self.end_date_time,
            course_id=self.course_id,
            room_id=self.room_id,
        )
    