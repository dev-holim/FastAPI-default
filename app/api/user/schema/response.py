from uuid import UUID
from pydantic import BaseModel


class DefaultResponse(BaseModel):
    id: UUID

class SignUpResponse(DefaultResponse):
    ...