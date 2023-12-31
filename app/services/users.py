import re
from typing import List
from uuid import UUID

from schemas.users import (
    UserCreateSchema,
    UserOutSchema,
    UserRegisterSchema,
    UserUpdateSchema,
    UserUpgradeSchema,
)
from utils.repository import AbstractDBRepository
from utils.auth import get_hashed_password


class UsersService:
    class UserNotFoundException(Exception):
        def __init__(self, login: str, *args: object) -> None:
            self.login = login
            super().__init__(*args)

    class UserExistsException(Exception):
        def __init__(self, login: str, *args: object) -> None:
            self.login = login
            super().__init__(*args)

    class NothingToUpdateException(Exception):
        ...

    def __init__(self, users_repo: AbstractDBRepository):
        self.users_repo: AbstractDBRepository = users_repo()

    async def get_user_by_login(self, login):
        user = await self.users_repo.find_one({"login": login})
        if not user:
            raise UsersService.UserNotFoundException(login)
        return user
    
    async def get_user_by_id(self, id):
        user = await self.users_repo.find_one({"id": id})
        if not user:
            raise UsersService.UserNotFoundException(id)
        return user.to_read_model()

    async def create_user(
        self, new_user: UserRegisterSchema
    ) -> UserOutSchema:
        await self.__raise_except_if_user_exists(new_user.login)
        create_dict = await self.__transform_values(new_user.model_dump(exclude_unset=True))
        create_user = UserCreateSchema(**create_dict)
        created_user = await self.users_repo.create_one(create_user.model_dump())
        return created_user

    async def update_user(
        self,
        current_user: UserOutSchema,
        new_values: UserUpdateSchema,
    ) -> UserOutSchema:
        update_dict = new_values.model_dump(exclude_unset=True)
        if login := update_dict.get("login") and login != current_user.login:
            await self.__raise_except_if_user_exists(login)
        upgrade_dct = await self.__transform_values(update_dict)
        upgrade_dct = await self.__remove_unchaneged_values(current_user, upgrade_dct)
        if not upgrade_dct:
            raise UsersService.NothingToUpdateException
        upgrade_user = UserUpgradeSchema(**upgrade_dct)
        upgraded_user = await self.users_repo.update_all(
            {"id": current_user.id}, upgrade_user.model_dump(exclude_unset=True)
        )
        return upgraded_user

    async def __raise_except_if_user_exists(self, login: str) -> None:
        try:
            await self.get_user_by_login(login)
        except UsersService.UserNotFoundException:
            ...
        else:
            raise UsersService.UserExistsException(login)

    async def __transform_values(self, dct: dict) -> dict:
        if dct.get("password", None):
            dct["hashed_password"] = get_hashed_password(dct.pop("password"))
        if dct.get("img_path", None):
            dct["img_path"] = str(dct["img_path"])
        return dct

    async def __remove_unchaneged_values(
        self, current_user: UserOutSchema, upgrade_dct: dict
    ) -> dict:
        for key, value in current_user.model_dump().items():
            if value and value == upgrade_dct.get(key, None):
                upgrade_dct.pop(key)
        return upgrade_dct

    async def delete_user_by_id(self, id: UUID) -> None:
        await self.users_repo.delete_all({"id": id})
