from datetime import datetime

import jwt

from config import settings
from schemas.tokens import TokenPayload, TokenSchema
from schemas.users import UserOutSchema, UserRegisterSchema
from services.users import UsersService
from utils.auth import create_access_token, create_refresh_token, verify_password


class AuthService:
    class IncorrectPasswordException(Exception):
        ...

    def __init__(
        self,
        users_service: UsersService,
    ):
        self.users_service: UsersService = users_service

    async def singup(self, new_user: UserRegisterSchema) -> UserOutSchema:
        user = await self.users_service.create_user(new_user)
        return user.to_read_model()

    async def login(self, form_data) -> TokenSchema:
        user = await self.users_service.get_user_by_login(form_data.username).to_db_model()
        if not verify_password(form_data.password, user.hashed_password):
            raise AuthService.IncorrectPasswordException
        return TokenSchema(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def refresh_tokens(self, refresh_token) -> TokenSchema:
        payload = jwt.decode(
            refresh_token,
            settings.auth.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.auth.ALGORITHM],
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise jwt.ExpiredSignatureError

        return TokenSchema(
            access_token=create_access_token(token_data.sub),
            refresh_token=create_refresh_token(token_data.sub),
        )
