from uuid import UUID, uuid4
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
# from schemas.courses import CourseOutSchema


class Courses(Base):
    __tablename__ = "courses"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    users: Mapped[List["UsersCourses"]] = relationship(back_populates="courses")

    # def to_read_model(self) -> CourseOutSchema:
    #     return CourseOutSchema(
    #         id=self.id,
    #         name=self.name,
    #     )