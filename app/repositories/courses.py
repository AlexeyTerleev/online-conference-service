from models.courses import Courses
from models.users_courses import UsersCourses
from utils.repository import SQLAlchemyRepository
from db.db import async_session_maker as db_async_session_maker
from sqlalchemy import asc, delete, insert, select, update
from uuid import UUID


class CoursesRepository(SQLAlchemyRepository):
    model = Courses

    async def join_course(self, user_id: UUID, course_id: UUID):
        async with db_async_session_maker() as session:
            stmt = insert(UsersCourses).values(user_id=user_id, course_id=course_id).returning(UsersCourses)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
        
    async def leave_course(self, user_id: UUID, course_id: UUID):
        async with db_async_session_maker() as session:
            stmt = delete(UsersCourses).filter_by(user_id=user_id, course_id=course_id)
            await session.execute(stmt)
            await session.commit()
            return None