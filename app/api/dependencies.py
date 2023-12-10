from repositories.users import UsersRepository
from repositories.courses import CoursesRepository
from repositories.rooms import RoomsRepository
from repositories.schedules import ScheduleRepository

from services.auth import AuthService
from services.users import UsersService
from services.courses import CourseService
from services.rooms import RoomService
from services.schedules import ScheduleService


def users_service():
    return UsersService(UsersRepository)

def course_service():
    return CourseService(CoursesRepository)

def room_service():
    return RoomService(RoomsRepository)

def schedule_service():
    return ScheduleService(ScheduleRepository)

def auth_service():
    return AuthService(
        UsersService(UsersRepository),
    )


