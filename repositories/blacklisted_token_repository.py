from typing import Optional

from ipomm_commons.models.blacklisted_token import BlacklistedToken
from ipomm_commons.repositories.basic_repository import Repository
from ipomm_commons.schemas.blacklisted_token import BlacklistedTokenCreate, BlacklistedTokenUpdate


class BlacklistedTokenRepository(
    Repository[BlacklistedToken, BlacklistedTokenCreate, BlacklistedTokenUpdate]
):
    def find_by_jti(self, *, jti: str) -> Optional[BlacklistedToken]:
        return self.model.objects(jti=jti).first()


blacklistedToken = BlacklistedTokenRepository(BlacklistedToken)
