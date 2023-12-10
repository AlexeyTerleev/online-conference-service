from typing import Annotated, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from schemas.users import (
    UserOutSchema,
)

from utils.oauth_bearer import get_current_user
from schemas.courses import CourseOutSchema, CourseRegisterSchema, CourseCreateSchema
from schemas.schedules import ScheduleRegisterSchema, ScheduleOutSchema
from services.courses import CourseService
from services.schedules import ScheduleService
from api.dependencies import course_service, schedule_service
from utils.roles import Role


router = APIRouter(
    prefix="/course",
    tags=["Courses"],
)


@router.get("s", response_model=List[CourseOutSchema])
async def get_all_courses(
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    course_service: Annotated[CourseService, Depends(course_service)],
):
    try:
        courses = await course_service.get_courses()
        return courses
    except Exception as e:
        raise e
    

@router.get("/{course_id}", response_model=CourseOutSchema)
async def get_course(
    course_id: UUID,
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    course_service: Annotated[CourseService, Depends(course_service)],
):
    try:
        course = await course_service.get_course_by_id(course_id)
        return course
    except CourseService.CourseNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course with id: [{course_id}] not found",
        )
    except Exception as e:
        raise e
    
@router.get("/{course_id}/schedule", response_model=List[ScheduleOutSchema])
async def get_course_schedule(
    course_id: UUID,
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    schedule_service: Annotated[ScheduleService, Depends(schedule_service)],
):
    try:
        schedule = await schedule_service.get_schedule_by_course_id(course_id)
        return schedule
    except ScheduleService.ScheduleNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Schedule to course with id: [{course_id}] not found",
        )
    except Exception as e:
        raise e
    

@router.post("/{course_id}/join", status_code=204)
async def get_course_schedule(
    course_id: UUID,
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    course_service: Annotated[CourseService, Depends(course_service)],
):
    try:
        await course_service.join_course_by_id(user.id, course_id)
    except Exception as e:
        raise e
    
@router.delete("/{course_id}/leave", status_code=204)
async def get_course_schedule(
    course_id: UUID,
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    course_service: Annotated[CourseService, Depends(course_service)],
):
    try:
        await course_service.leave_course_by_id(user.id, course_id)
    except Exception as e:
        raise e
    

@router.post("", response_model=CourseOutSchema)
async def create_course(
    course: CourseRegisterSchema,
    user: Annotated[UserOutSchema, Depends(get_current_user)],
    course_service: Annotated[CourseService, Depends(course_service)],
    schedule_service: Annotated[ScheduleService, Depends(schedule_service)],
):
    try:
        if user.role != Role.teacher:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied",
            )
        created_course = await course_service.create_course(course)
        schedules = await schedule_service.create_course_schedule(created_course.id, course.schedules)
        return created_course
    except Exception as e:
        raise e




