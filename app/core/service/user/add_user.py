from uuid import UUID
from fastapi import Depends

from app.abc.repository.base import UoW
from app.adapter.repository.rdb import RDBUoW, UserRepositoryImpl
from app.adapter.repository.rdb.entities import User
from app.core.exception import ALREADY_EXIST_EXCEPTION, ExceptionDetail
from app.security.crypt import PasswordManager, get_password_manager

from .._base_ import Service
from app.core.enums import UserRole


class AddUserService(Service):

    def __init__(
            self,
            uow: UoW = Depends(
                RDBUoW(
                    repositories=[
                        UserRepositoryImpl
                    ]
                )
            ),
        pm: PasswordManager = Depends(
            get_password_manager
        )
    ):
        self.uow = uow
        self.password_manager = pm

    async def __call__(self, name: str, email: str, password: str):
        async with self.uow.enter() as uow:
            if _ := await uow.user_repository.find_by_email(email):
                raise ALREADY_EXIST_EXCEPTION(
                    ExceptionDetail.USER_ALREADY_EXIST
                )

            user_ = await uow.user_repository.save(
                User(
                    name=name,
                    email=email,
                    password=self.password_manager.hash(password),
                    role=UserRole.USER.value
                )
            )

            return {"id":user_.id}