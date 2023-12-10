from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from api.dependencies import users_service
from config import settings
from schemas.users import UserOutSchema
from schemas.tokens import TokenPayload
from services.users import UsersService

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="./auth/login", scheme_name="JWT")


async def get_current_user(
    users_service: Annotated[UsersService, Depends(users_service)],
    token: Annotated[str, Depends(reuseable_oauth)],
) -> UserOutSchema:
    try:
        payload = jwt.decode(
            token, settings.auth.JWT_SECRET_KEY, algorithms=[settings.auth.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.exceptions.DecodeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user = await users_service.get_user_by_id(token_data.sub)
    except Exception as e:
        raise e
    return user
