from typing import Annotated

from fastapi import APIRouter, Depends

from schemas.users import (
    UserOutSchema,
)

from utils.oauth_bearer import get_current_user


router = APIRouter(
    prefix="/me",
    tags=["Authorization"],
)


@router.get("", response_model=UserOutSchema)
async def me_get(
    user: Annotated[UserOutSchema, Depends(get_current_user)],
):
    try:
        return user
    except Exception as e:
        raise e




