from models.courses import Courses
from utils.repository import SQLAlchemyRepository


class CoursesRepository(SQLAlchemyRepository):
    model = Courses