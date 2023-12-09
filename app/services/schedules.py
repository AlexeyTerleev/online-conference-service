from typing import List
from uuid import UUID

from sqlalchemy import asc, desc

from schemas.schedules import ScheduleCreateSchema, ScheduleOutSchema, ScheduleRegisterSchema

from utils.repository import AbstractDBRepository


class ScheduleService:

    class ScheduleNotFoundException(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    def __init__(self, shedules_repo: AbstractDBRepository):
        self.shedules_repo: AbstractDBRepository = shedules_repo()

    async def get_schedule_by_course_id(self, course_id: UUID) -> List[ScheduleOutSchema]:
        schedules = await self.shedules_repo.find_all({"course_id": course_id})
        if not schedules:
            raise ScheduleService.ScheduleNotFoundException()
        return [schedule.to_read_model() for schedule in schedules]

    async def create_course_schedule(
        self, course_id: UUID, new_schedules: List[ScheduleRegisterSchema]
    ) -> List[ScheduleOutSchema]:
        create_shedules = [
            ScheduleCreateSchema(course_id=course_id, **new_schedule.model_dump()) 
            for new_schedule in new_schedules
        ]
        created_shedules = [
            await self.shedules_repo.create_one(schedule.model_dump()) 
            for schedule in create_shedules
        ]
        return [created_shedule.to_read_model() for created_shedule in created_shedules]
    
    async def delete_course_schedule(self, course_id: UUID) -> None:
        await self.shedules_repo.delete_all({"course_id": course_id})

    async def delete_schedule_row_by_id(self, id: UUID) -> None:
        await self.shedules_repo.delete_all({"id": id})

    async def set_or_update_schedule_room(self, id: UUID, room_id: UUID) -> None:
        await self.shedules_repo.update_all({"id": id}, {"room_id": room_id})

