from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class BlacklistedTokenCreate(BaseModel):
    jti: str


class BlacklistedTokenUpdate(BaseModel):
    jti: str


class BlacklistedToken(BaseModel):
    jti: Optional[str]
    id: Optional[str] = None

    @validator("id", pre=True)
    def validate_id(cls, v):
        if not isinstance(v, str):
            try:
                return str(v)
            except Exception as err:
                raise ValueError(f"Could not parse id into valid ObjectId: {err}")

        return v

    class Config:
        orm_mode = True


# Additional properties stored in DB
class BlacklistedTokenInDB(BaseModel):
    jti: str
    created_at: datetime
    updated_at: datetime
