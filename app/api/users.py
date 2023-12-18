from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from schemas.users import UserOutSchema
from schemas.schedules import ScheduleOutSchema
from schemas.courses import CourseIdSchema

from utils.oauth_bearer import get_current_user
from services.users import UsersService
from services.schedules import ScheduleService
from services.courses import CourseService

from api.dependencies import users_service, schedule_service, course_service
from utils.roles import Role


router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.get("/me", response_model=UserOutSchema)
async def me_get(
    user: Annotated[UserOutSchema, Depends(get_current_user)],
):
    try:
        return user
    except Exception as e:
        raise e
    

@router.get("/me/schedule", response_model=List[ScheduleOutSchema])
async def me_schedule_get(
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    schedule_service: Annotated[ScheduleService, Depends(schedule_service)],
    course_service: Annotated[CourseService, Depends(course_service)],
):
    try:
        if user.role == Role.student:
            courses = user.courses
        else: 
            courses = await course_service.get_owner_courses(user.id)
        schedule = []
        for course in courses:
            schedule += await schedule_service.get_schedule_by_course_id(course.id)
        return schedule
    except Exception as e:
        raise e
    
@router.get("/me/courses", response_model=List[CourseIdSchema])
async def me_schedule_get(
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    course_service: Annotated[CourseService, Depends(course_service)],
):
    try:
        if user.role == Role.student:
            return user.courses
        else:
            courses = await course_service.get_owner_courses(user.id)
            return courses
    except Exception as e:
        raise e


@router.get("/{user_id}", response_model=UserOutSchema)
async def users_get(
    user_id: UUID,
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    users_service: Annotated[UsersService, Depends(users_service)],
):
    try:
        aim_user = await users_service.get_user_by_id(user_id)
        return aim_user
    except UsersService.UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id: [{user_id}] not found",
        )
    except Exception as e:
        raise e





