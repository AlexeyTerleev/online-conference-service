from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, validator


class RoomSchema(BaseModel):
    private: bool
    password: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @validator('password', pre=True, always=True)
    def validate_password(cls, value, values):
        if values.get('private') and not value:
            raise ValueError("Password is required for private rooms")
        return value


class RoomRegisterSchema(RoomSchema):
    ...


class RoomCreateSchema(RoomSchema):
    ...

class RoomOutSchema(RoomSchema):
    id: UUID


