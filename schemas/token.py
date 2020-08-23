import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from typing_extensions import Literal


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    exp: datetime
    jti: str = str(uuid.uuid4())
    iat: datetime = datetime.utcnow()
    token_type: Literal["access", "refresh"]
    sub: Optional[str] = None
