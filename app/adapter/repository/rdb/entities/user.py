from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ._base import Base


class User(Base):
    __tablename__ = 'tbl_user'

    id = Column('id', UUID(as_uuid=True), primary_key=True, nullable=False)
    name = Column('name', String(150), nullable=False)
    email = Column('email', String(150), nullable=False, unique=True)
    password = Column('password', String(128), nullable=False)
    role = Column('role', String(20), nullable=False)
    is_active = Column('is_active', Boolean, nullable=False, default=True)
    is_approved = Column('is_approved', Boolean, nullable=False, default=False)
    created_at = Column('created_at', DateTime, nullable=False, default=datetime.now)
    approved_at = Column('approved_at', DateTime, nullable=True)

    # credit = relationship(
    #     'Credit',
    #     lazy='noload',
    #     uselist=False,
    #     backref='user',
    #     foreign_keys='Credit.user_id'
    # )

    def __init__(
            self,
            name: str,
            role: str,
            email: str,
            password: str,
            is_active: bool = True,
            is_approved: bool = False
    ):
        self.id = uuid4()
        self.name = name
        self.role = role
        self.email = email
        self.password = password
        self.is_active = is_active
        self.is_approved = is_approved
        self.created_at = datetime.now()
