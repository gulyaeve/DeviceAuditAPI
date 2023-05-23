from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings
from app.exceptions import WrongTokenException

# Placeholder for a database containing valid token values
known_tokens = {settings.TOKEN_BEARER}
get_bearer_token = HTTPBearer(auto_error=False)


async def get_token(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
) -> str:
    # Simulate a database query to find a known token
    if auth is None or (token := auth.credentials) not in known_tokens:
        raise WrongTokenException
    return token
