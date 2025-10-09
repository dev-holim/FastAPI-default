from fastapi import Depends

from app.abc.client.jwt import JWTEncodeClient
from app.abc.repository.base import UoW
from app.adapter.client.auth_client import AuthClient
from app.adapter.client.jwt_encoder import JWTEncoder
from app.adapter.repository.cache import CacheUoW, UserTokenRepo
from app.adapter.repository.rdb import RDBUoW, UserRepositoryImpl
from app.core.exception import ALREADY_EXIST_EXCEPTION, ExceptionDetail
from app.security.crypt import PasswordManager, get_password_manager

from .._base_ import Service


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
            cache_uow: UoW = Depends(
                CacheUoW(
                    repositories=[
                        UserTokenRepo
                    ]
                )
            ),
            auth_client = Depends(AuthClient),
            jwt_client: JWTEncodeClient = Depends(JWTEncoder),
            pm: PasswordManager = Depends(
                get_password_manager
            )
    ):
        self.rdb_uow = rdb_uow
        self.cache_uow = cache_uow
        self.auth_client = auth_client
        self.jwt_client = jwt_client
        self.password_manager = pm

    async def __call__(self, email: str, password: str):
        return await self.auth_client.login(email, password)

        async with self.rdb_uow.enter() as rdb_uow:
            user_ = await rdb_uow.user_repository.find_by_email(email)

            if user_ is None:
                raise ALREADY_EXIST_EXCEPTION(
                    ExceptionDetail.USER_NOT_FOUND
                )

            if not self.password_manager.verify(password, user_.password):
                raise ALREADY_EXIST_EXCEPTION(
                    ExceptionDetail.USER_PASSWORD_NOT_MATCH
                )

            access_token, access_expired_at = self.jwt_client.access_token(
                str(user_.id)
            )

            refresh_token, refresh_expired_at = self.jwt_client.refresh_token(
                str(user_.id)
            )

            async with self.cache_uow.enter() as cache_uow:
                await cache_uow.user_token_repo.set_user_hash(
                    str(user_.id),
                    email
                )

            return {
                "access_token":access_token,
                "access_expired_at":access_expired_at,
                "refresh_token":refresh_token,
                "refresh_expired_at":refresh_expired_at
            }