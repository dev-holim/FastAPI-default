from typing import Optional
from uuid import UUID

from fastapi import Cookie, Depends, Header, HTTPException

from app.abc.client.jwt import JWTPayload
from app.adapter.client.jwt_decoder import JWTDecoder
from app.core.exception import AUTHENTICATION_ERROR_EXCEPTION, ExceptionDetail


class Authorization:

    def __init__(self):
        ...

    def __call__(
            self,
            token_cookie: str = Cookie(alias='access_token', default=None),
            token_header: Optional[str] = Header(alias='Authorization', default=None),
            jwt_decoder: JWTDecoder = Depends(JWTDecoder)
    ) -> UUID:
        if token_header is None:
            # Cookie
            if token_cookie is None:
                raise AUTHENTICATION_ERROR_EXCEPTION(
                    ExceptionDetail.TOKEN_NOT_FOUND
                )

            _, suffix = token_cookie.split(' ')

        else:
            split_token = token_header.split(' ')

            if len(split_token) == 1:
                raise AUTHENTICATION_ERROR_EXCEPTION(
                    ExceptionDetail.INVALID_TOKEN_NO_SUFFIx
                )

            bearer, suffix = split_token

        payload: JWTPayload = jwt_decoder.access_token(
            token=suffix,
        )

        return UUID(payload.sub)
