from db.db import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from uuid import UUID, uuid4


class Rooms(Base):
    __tablename__ = "rooms"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    private: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str] = mapped_column(nullable=True)

    