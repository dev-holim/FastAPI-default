from uuid import UUID
from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.config import get_async_database_url
from app.core.service import Service, GetMyInformationService

user_router = APIRouter(
    tags=['User']
)

@user_router.post('/login')
async def login_proc(
):
    return get_async_database_url()

@user_router.get(
    summary='내 정보 조회',
    description='사용하고 있는 계정의 정보들을 제공',
    # response_model=MyInformationResponse,
    status_code=HTTPStatus.OK,
    path='/me'
)
async def get_user_information(
        # user_id: UUID = Depends(Authorization()),
        service: Service = Depends(GetMyInformationService)
):
    user_id = ""
    return await service(user_id)