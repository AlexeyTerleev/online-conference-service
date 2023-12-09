from models.rooms import Rooms
from utils.repository import SQLAlchemyRepository


class RoomsRepository(SQLAlchemyRepository):
    model = Rooms