from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader, APIKey
from starlette.status import HTTP_401_UNAUTHORIZED

import settings

api_key_header = APIKeyHeader(name='X-API-KEY', auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key == settings.X_API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
