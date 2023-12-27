from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies import room_service, schedule_service
from schemas.users import UserOutSchema
from services.rooms import RoomService
from services.schedules import ScheduleService
from schemas.rooms import RoomRegisterSchema, RoomOutSchema
from utils.oauth_bearer import get_current_user


router = APIRouter(
    prefix="/schedule",
    tags=["Schedule"],
)

@router.post("/{schedule_id}/room")
async def create_room(
    schedule_id: UUID,
    new_room: RoomRegisterSchema,
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    room_service: Annotated[RoomService, Depends(room_service)],
    schedule_service: Annotated[ScheduleService, Depends(schedule_service)],
):
    try:
        schedule = await schedule_service.get_schedule_id(schedule_id)
        if user.id != schedule.course.owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied",
            )
        room = await room_service.create_room(new_room)
        await schedule_service.set_or_update_schedule_room(schedule.id, room.id)
    except Exception as e:
        raise e
    
@router.get("/{schedule_id}/room", response_model=RoomOutSchema)
async def get_room(
    schedule_id: UUID,
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    room_service: Annotated[RoomService, Depends(room_service)],
    schedule_service: Annotated[ScheduleService, Depends(schedule_service)],
):
    try:
        schedule = await schedule_service.get_schedule_id(schedule_id)
        room = await room_service.get_room_by_id(schedule.room_id)
        return room
    except Exception as e:
        raise e