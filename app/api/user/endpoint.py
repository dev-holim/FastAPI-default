from uuid import UUID
from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.api.user.schema.reqest import SignUpRequest
from app.api.user.schema.response import SignUpResponse
from app.config import get_async_database_url
from app.core.service import Service, AddUserService
from app.security.auth import Authorization

user_router = APIRouter(
    tags=['User']
)

@user_router.post('/login')
async def login_proc(
    user_id: UUID = Depends(Authorization()),
):
    return user_id



@user_router.post(
    name="user:register",
    summary='회원가입',
    description='회원 가입 프로세스',
    response_model=SignUpResponse,
    status_code=HTTPStatus.OK,
    path='/sign-up'
)
async def get_user_information(
    request: SignUpRequest,
    service: Service = Depends(AddUserService)
):
    return await service(
        name=request.name,
        email=request.email,
        password=request.password,
    )