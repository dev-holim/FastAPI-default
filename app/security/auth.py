from typing import Optional
from uuid import UUID

from fastapi import Cookie, Depends, Header, HTTPException

from app.abc.client.jwt import JWTPayload
from app.adapter.client.jwt_decoder import JWTDecoder
from app.core.exception import AUTHENTICATION_ERROR_EXCEPTION, ExceptionDetail
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class Authorization:

    def __init__(self):
        ...

    def __call__(
            self,
            credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()), # Authorization: Bearer <JWT>
            # token_cookie: Optional[str] = Cookie(alias='access_token', default=None),
            # token_header: Optional[str] = Header(alias='Authorization', default=None),
            jwt_decoder: JWTDecoder = Depends(JWTDecoder)
    ) -> UUID:
        if not credentials:
            raise AUTHENTICATION_ERROR_EXCEPTION(
                ExceptionDetail.TOKEN_NOT_FOUND
            )

        payload: JWTPayload = jwt_decoder.access_token(
            token=credentials.credentials,
        )

        return UUID(payload.sub)
