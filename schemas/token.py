import datetime
from pydantic import BaseModel
from core.config import settings

ACCESS_TOKEN_LIFETIME = settings.ACCESS_TOKEN_LIFETIME
REFRESH_TOKEN_LIFETIME = settings.REFRESH_TOKEN_LIFETIME


class BaseTokenSchema(BaseModel):
    """
    Token Model
    """
    user_id: str
    iat: str = datetime.datetime.utcnow()
    jti: str

