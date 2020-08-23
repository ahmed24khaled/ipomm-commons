from typing import Any, Dict, Optional, Union
from pydantic import BaseSettings, validator
import os


class Settings(BaseSettings):
    AUTH_API: str
    JWT_BLACKLIST_ENABLED: bool = False
    JWT_ALGORITHM: str = "RS256"
    JWT_KEYS_PATH: str
    JWT_PUBLIC_KEY_NAME: str

    JWT_PUBLIC_KEY: Optional[str]

    @validator("JWT_PUBLIC_KEY", pre=True)
    def set_public_key(cls, v: str, values: Dict[str, Any]) -> Union[str, bytes]:
        if v is not None and v != "":
            return v
        else:
            public_key_path = "{0}{1}".format(values.get("JWT_KEYS_PATH"), values.get("JWT_PUBLIC_KEY_NAME"))
            if os.path.isfile(public_key_path):
                with open(public_key_path, "rb") as f:
                    public_key = f.read()
                    return public_key
            else:
                # check shared volume or get public key from auth provider
                raise FileNotFoundError("{0} not found".format(public_key_path))

    class Config:
        case_sensitive = True


settings = Settings()
