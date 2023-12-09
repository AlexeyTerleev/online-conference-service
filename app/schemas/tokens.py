from pydantic import BaseModel, ConfigDict, validator


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenSchema(BaseModel):
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

    model_config = ConfigDict(from_attributes=True)