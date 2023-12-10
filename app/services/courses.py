import re
from typing import List
from uuid import UUID

from sqlalchemy import asc, desc

from schemas.courses import CourseRegisterSchema, CourseCreateSchema, CourseOutSchema

from utils.repository import AbstractDBRepository


class CourseService:

    class CourseNotFoundException(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    def __init__(self, courses_repo: AbstractDBRepository):
        self.courses_repo: AbstractDBRepository = courses_repo()

    async def get_course_by_id(self, id):
        course = await self.courses_repo.find_one({"id": id})
        if not course:
            raise CourseService.CourseNotFoundException()
        return course

    async def create_course(
        self, new_course: CourseRegisterSchema
    ) -> CourseOutSchema:
        create_user = CourseCreateSchema(**new_course.model_dump())
        created_user = await self.courses_repo.create_one(create_user.model_dump())
        return created_user.to_read_model()
    
    async def delete_course_by_id(self, id: UUID) -> None:
        await self.courses_repo.delete_all({"id": id})

    async def get_courses(self, filter_by: dict = None) -> List[CourseOutSchema]:
        courses = await self.courses_repo.find_all(filter_by if filter_by else {})
        return [course.to_read_model() for course in courses]
    
    async def join_course_by_id(self, user_id: UUID, course_id: UUID) -> None:
        await self.courses_repo.join_course(user_id, course_id)

    async def leave_course_by_id(self, user_id: UUID, course_id: UUID) -> None:
        await self.courses_repo.leave_course(user_id, course_id)