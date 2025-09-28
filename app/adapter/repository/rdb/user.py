from uuid import UUID
from sqlalchemy import select

from app.abc.repository.user import UserRepository

from .entities import User
from ._base import RDBRepository


class UserRepositoryImpl(RDBRepository, UserRepository):
    __repo_name__ = 'user_repository'

    async def find_by_id(self, id_: UUID):
        stmt = select(User).where(User.id == id_)

        return await self.session.scalar(stmt)

    async def find_by_email(self, email: str):
        stmt = select(User).where(User.email == email)

        return await self.session.scalar(stmt)
