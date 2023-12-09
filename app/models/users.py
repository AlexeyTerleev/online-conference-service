from uuid import UUID, uuid4
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
from utils.roles import Role
from models.users_courses import UsersCourses


from schemas.base import UserIdSchema
from schemas.users import UserOutSchema, UserDbSchema


class Users(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    login: Mapped[str]
    personal_info: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str]
    img_path: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[Role]

    courses: Mapped[List["Courses"]] = relationship(
        secondary="users_courses", back_populates="users", viewonly=True, lazy="selectin",
    )
    course_associations: Mapped[List["UsersCourses"]] = relationship(
        back_populates="user"
    )

    def to_id_model(self) -> UserIdSchema:
        return UserIdSchema(
            id=self.id,
            name=self.name,
            login=self.login,
            personal_info=self.personal_info,
            img_path=self.img_path,
            role=self.role,
        )
    
    def to_db_model(self) -> UserDbSchema:
        return UserDbSchema(
            id=self.id,
            name=self.name,
            login=self.login,
            personal_info=self.personal_info,
            img_path=self.img_path,
            role=self.role,
            hashed_password=self.hashed_password,
        )

    def to_read_model(self) -> UserOutSchema:
        return UserOutSchema(
            id=self.id,
            name=self.name,
            login=self.login,
            personal_info=self.personal_info,
            img_path=self.img_path,
            role=self.role,
            courses=[course.to_id_model() for course in self.courses],
        )

