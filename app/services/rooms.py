from typing import List
from uuid import UUID

from sqlalchemy import asc, desc

from schemas.rooms import RoomRegisterSchema, RoomCreateSchema, RoomOutSchema, RoomCredsSchema

from utils.repository import AbstractDBRepository


class RoomService:

    class RoomNotFoundException(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    def __init__(self, room_repo: AbstractDBRepository):
        self.room_repo: AbstractDBRepository = room_repo()

    async def get_room_by_id(self, id):
        room = await self.room_repo.find_one({"id": id})
        if not room:
            raise RoomService.RoomNotFoundException()
        return room

    async def create_room(
        self, new_room: RoomRegisterSchema
    ) -> RoomOutSchema:
        create_room = RoomCreateSchema(**new_room.model_dump())
        created_room = await self.room_repo.create_one(create_room.model_dump())
        return created_room.to_read_model()
    
    async def delete_room_by_id(self, id: UUID) -> None:
        await self.room_repo.delete_all({"id": id})

    async def join_room(
        self, creds: RoomCredsSchema
    ) -> bool:
        room = await self.get_room_by_id(creds.key)
        return not room.private or room.password == creds.password
    