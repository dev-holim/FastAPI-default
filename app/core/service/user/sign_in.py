from uuid import UUID

from fastapi import Depends

from app.abc.client.jwt import JWTEncodeClient
from app.abc.repository.base import UoW
from app.adapter.client.jwt_encoder import JWTEncoder
from app.adapter.repository.rdb import RDBUoW, UserRepositoryImpl
from app.adapter.repository.rdb.entities import User
from app.core.exception import ALREADY_EXIST_EXCEPTION, ExceptionDetail
from app.security.crypt import PasswordManager, get_password_manager

from .._base_ import Service
from app.core.enums import UserRole


class SignInService(Service):

    def __init__(
            self,
            rdb_uow: UoW = Depends(
                RDBUoW(
                    repositories=[
                        UserRepositoryImpl
                    ]
                )
            ),
            jwt_client: JWTEncodeClient = Depends(JWTEncoder)
    ):
        self.rdb_uow = rdb_uow
        self.jwt_client = jwt_client

    async def __call__(self, uid: UUID):
        async with self.rdb_uow.enter() as rdb_uow:
            user_ = await rdb_uow.user_repository.find_by_id(uid)

            if user_ is None:
                raise ALREADY_EXIST_EXCEPTION(
                    ExceptionDetail.USER_NOT_FOUND
                )

            access_token, access_expired_at = self.jwt_client.access_token(
                str(user_.id)
            )

            refresh_token, refresh_expired_at = self.jwt_client.refresh_token(
                str(user_.id)
            )

            return {
                "id":user_.id,
                "access_token":access_token,
                "access_expired_at":access_expired_at,
                "refresh_token":refresh_token,
                "refresh_expired_at":refresh_expired_at
            }