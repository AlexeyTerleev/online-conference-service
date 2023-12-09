from models.schedules import Schedules
from utils.repository import SQLAlchemyRepository


class ScheduleRepository(SQLAlchemyRepository):
    model = Schedules