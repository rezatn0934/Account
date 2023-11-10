import datetime
from pydantic import BaseModel
from config.config import settings

ACCESS_TOKEN_LIFETIME = settings.ACCESS_TOKEN_LIFETIME
REFRESH_TOKEN_LIFETIME = settings.REFRESH_TOKEN_LIFETIME


class BaseTokenSchema(BaseModel):
    """
    Token Model
    """
    user_id: str
    iat: datetime.datetime = datetime.datetime.utcnow()
    jti: str


class AccessToken(BaseTokenSchema):
    token_type: str = 'access'
    exp: datetime.datetime = datetime.datetime.utcnow() + datetime.timedelta(seconds=ACCESS_TOKEN_LIFETIME)


class RefreshToken(BaseTokenSchema):
    token_type: str = 'refresh'
    exp: datetime.datetime = datetime.datetime.utcnow() + datetime.timedelta(seconds=REFRESH_TOKEN_LIFETIME)


class OtpToken(BaseModel):
    token: str
