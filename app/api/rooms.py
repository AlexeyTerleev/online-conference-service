from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies import room_service
from schemas.users import UserOutSchema
from services.rooms import RoomService
from services.schedules import ScheduleService
from schemas.rooms import RoomCredsSchema, RoomRegisterSchema, RoomOutSchema
from utils.oauth_bearer import get_current_user
from pydantic import create_model


router = APIRouter(
    prefix="/room",
    tags=["Room"],
)

@router.get("/{room_id}", response_model=RoomOutSchema)
async def get_room(
    room_id: UUID,
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    room_service: Annotated[RoomService, Depends(room_service)],
):
    try:
        room = await room_service.get_room_by_id(room_id)
        return room
    except Exception as e:
        raise e
    
@router.post("", response_model=RoomOutSchema)
async def create_room(
    new_room: RoomRegisterSchema,
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    room_service: Annotated[RoomService, Depends(room_service)],
):
    try:
        room = await room_service.create_room(new_room)
        return room
    except Exception as e:
        raise e
    

@router.post("/join")
async def room_join(
    room_creds: RoomCredsSchema,
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    room_service: Annotated[RoomService, Depends(room_service)],
):
    try:
        access = await room_service.join_room(room_creds)
        return {"access": access}
    except Exception as e:
        raise e
    