import re
from typing import List
from uuid import UUID

from sqlalchemy import asc, desc

from schemas.courses import CourseRegisterSchema, CourseCreateSchema, CourseOutSchema, CourseIdSchema

from utils.repository import AbstractDBRepository


class CourseService:

    class CourseNotFoundException(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)
    
    class AlreadyJoinedException(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)
    
    class NotJoinedException(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    def __init__(self, courses_repo: AbstractDBRepository):
        self.courses_repo: AbstractDBRepository = courses_repo()

    async def get_course_by_id(self, id):
        course = await self.courses_repo.find_one({"id": id})
        if not course:
            raise CourseService.CourseNotFoundException
        return course

    async def create_course(
        self, owner_id: UUID, new_course: CourseRegisterSchema
    ) -> CourseOutSchema:
        create_course = CourseCreateSchema(owner_id=owner_id, **new_course.model_dump())
        created_course = await self.courses_repo.create_one(create_course.model_dump())
        return created_course.to_read_model()
    
    async def get_owner_courses(
        self, owner_id: UUID
    ) -> CourseIdSchema:
        courses = await self.courses_repo.find_all({"owner_id": owner_id})
        return [course.to_id_model() for course in courses]

    async def delete_course_by_id(self, id: UUID) -> None:
        await self.courses_repo.delete_all({"id": id})

    async def get_courses(self, filter_by: dict = None) -> List[CourseOutSchema]:
        courses = await self.courses_repo.find_all(filter_by if filter_by else {})
        return [course.to_read_model() for course in courses]
    
    async def join_course_by_id(self, user_id: UUID, course_id: UUID) -> None:
        course = await self.get_course_by_id(course_id)
        if user_id in [user.id for user in course.users]:
            raise CourseService.AlreadyJoinedException
        await self.courses_repo.join_course(user_id, course_id)

    async def leave_course_by_id(self, user_id: UUID, course_id: UUID) -> None:
        course = await self.get_course_by_id(course_id)
        if user_id not in [user.id for user in course.users]:
            raise CourseService.AlreadyJoinedException
        await self.courses_repo.leave_course(user_id, course_id)