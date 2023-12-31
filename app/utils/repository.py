from abc import ABC, abstractmethod
from typing import Callable

from sqlalchemy import asc, delete, insert, select, update


from config import settings
from db.db import async_session_maker as db_async_session_maker


class AbstractDBRepository(ABC):
    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def find_one():
        raise NotImplementedError

    @abstractmethod
    async def create_one():
        raise NotImplementedError

    @abstractmethod
    async def update_all():
        raise NotImplementedError

    @abstractmethod
    async def delete_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractDBRepository):
    model = None

    async def find_all(
        self,
        filter_by: dict,
        sorted_by: str = None,
        order_func: Callable = asc,
        limit: int = None,
        offset: int = None,
    ):
        async with db_async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            if sorted_by:
                stmt = stmt.order_by(order_func(sorted_by))
            if limit:
                stmt = stmt.limit(limit)
            if offset:
                stmt = stmt.offset(offset)
            res = await session.execute(stmt)
            res = [row[0] for row in res.unique().all()]
            return res

    async def find_one(self, filter_by: dict):
        async with db_async_session_maker() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            res = res.first()
            return None if res is None else res[0]

    async def create_one(self, values: dict):
        async with db_async_session_maker() as session:
            stmt = insert(self.model).values(**values).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def update_all(self, filter_by: dict, new_values: dict):
        async with db_async_session_maker() as session:
            stmt = (
                update(self.model)
                .filter_by(**filter_by)
                .values(**new_values)
                .returning(self.model)
            )
            updated_user = await session.execute(stmt)
            await session.commit()
            updated_user = updated_user.unique().scalar_one()
            return updated_user

    async def delete_all(self, filter_by: dict):
        async with db_async_session_maker() as session:
            stmt = delete(self.model).filter_by(**filter_by)
            await session.execute(stmt)
            await session.commit()
            return None

