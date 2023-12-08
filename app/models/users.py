from uuid import UUID, uuid4
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Base
# from schemas.users import UserOutSchema
from utils.roles import Role


class Users(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    login: Mapped[str]
    personal_info: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str]
    img_path: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[Role]
    courses: Mapped[List["UsersCourses"]] = relationship(back_populates="users")

    # def to_read_model(self) -> UserOutSchema:
    #     return UserOutSchema(
    #         id=self.id,
    #         name=self.name,
    #         login=self.login,
    #         personal_info=self.personal_info,
    #         hashed_password=self.hashed_password,
    #         img_path=self.img_path,
    #         role=self.role,
    #     )

