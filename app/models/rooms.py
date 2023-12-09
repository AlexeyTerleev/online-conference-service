from db.db import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from uuid import UUID, uuid4
from schemas.rooms import RoomOutSchema


class Rooms(Base):
    __tablename__ = "rooms"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    private: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str] = mapped_column(nullable=True)

    def to_read_model(self) -> RoomOutSchema:
        return RoomOutSchema(
            id=self.id,
            private=self.private,
            password=self.password,
        )

    