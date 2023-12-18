from uuid import UUID, uuid4
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from models.users_courses import UsersCourses

from schemas.base import CourseIdSchema
from schemas.courses import CourseOutSchema, CourseDbSchema


class Courses(Base):
    __tablename__ = "courses"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    info: Mapped[str]
    owner_id: Mapped[UUID]

    users: Mapped[List["Users"]] = relationship(
        secondary="users_courses", back_populates="courses", viewonly=True, lazy="selectin",
    )
    user_associations: Mapped[List["UsersCourses"]] = relationship(
        back_populates="course"
    )
    schedules: Mapped[List["Schedules"]] = relationship(
        back_populates="course", lazy="selectin",
    )

    def to_id_model(self) -> CourseIdSchema:
        return CourseIdSchema(
            id=self.id,
            name=self.name,
            info=self.info,
            owner_id=self.owner_id,
        )

    def to_db_model(self) -> CourseDbSchema:
        return CourseDbSchema(
            id=self.id,
            name=self.name,
            info=self.info,
            owner_id=self.owner_id,
        )

    def to_read_model(self) -> CourseOutSchema:
        return CourseOutSchema(
            id=self.id,
            name=self.name,
            info=self.info,
            users=[user.to_id_model() for user in self.users],
            owner_id=self.owner_id,
        )