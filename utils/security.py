from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from ipomm_commons import repositories
from ipomm_commons.schemas import TokenPayload
from ipomm_commons.utils import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=settings.AUTH_API)


def verify_token_not_blacklisted(token_id: str) -> bool:
    if not settings.JWT_BLACKLIST_ENABLED:
        return True
    if repositories.blacklistedToken.find_by_jti(jti=token_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked"
        )
    return True


def verify_access_token(token: str = Depends(reusable_oauth2)) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.JWT_PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate Token"
        )
    if token_data.token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="{0}_token is different from expected token type: Access".format(
                token_data.token_type
            ),
        )

    verify_token_not_blacklisted(token_data.jti)
    # Todo verify token.sub.tenant == request.state.tenantId and save userId in request.state.userId
    return token_data
