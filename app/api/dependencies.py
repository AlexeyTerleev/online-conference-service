from repositories.users import UsersRepository
from repositories.courses import CoursesRepository
from repositories.rooms import RoomsRepository
from repositories.schedules import ScheduleRepository

from services.auth import AuthService
from services.users import UsersService


def users_service():
    return UsersService(UsersRepository)


def auth_service():
    return AuthService(
        UsersService(UsersRepository),
    )


