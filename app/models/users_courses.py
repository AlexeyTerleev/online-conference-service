from db.db import Base
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class UsersCourses(Base):
    __tablename__ = "users_courses"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    course_id: Mapped[UUID] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    extra_data: Mapped[Optional[str]]
    user: Mapped["Users"] = relationship(back_populates="course_associations")
    course: Mapped["Courses"] = relationship(back_populates="user_associations")