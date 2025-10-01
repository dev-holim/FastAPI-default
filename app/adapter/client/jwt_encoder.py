from uuid import UUID
from typing import Tuple
from dataclasses import asdict
from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings, JWTConfig
from app.abc.client.jwt import JWTEncodeClient, JWTPayload


class JWTEncoder(JWTEncodeClient):
    def __init__(self, config: JWTConfig = settings.jwt):
        # TODO: setting jwt => prod, stage, develop으로 구성
        self.config = config

    def _encode(
        self,
        key: str,
        user_id: str,
        token_type: str,
        expire_sec: int
    ) -> Tuple[str, float]:
        now = datetime.now()
        remain = timedelta(seconds=expire_sec)

        expire = now + remain
        expired_at = expire.timestamp()

        token = jwt.encode(
            payload=asdict(
                JWTPayload(
                    sub=user_id,
                    typ=token_type,
                    exp=expired_at
                )
            ),
            key=key,
            algorithm=self.config.ALGORITHM
        )

        return token, expired_at

    def access_token(self, user_id: UUID) -> Tuple[str, float]:
        key = self.config.ACCESS_KEY
        token_type = self.config.ACCESS_TYP
        expire_sec = self.config.ACCESS_EXP

        token, expired_at = self._encode(
            key=key,
            user_id=str(user_id),
            token_type=token_type,
            expire_sec=expire_sec
        )

        return token, expired_at

    def refresh_token(self, user_id: UUID) -> Tuple[str, float]:
        key = self.config.REFRESH_KEY
        token_type = self.config.REFRESH_TYP
        expire_sec = self.config.REFRESH_EXP

        token, expired_at = self._encode(
            key=key,
            user_id=str(user_id),
            token_type=token_type,
            expire_sec=expire_sec
        )

        return token, expired_at
