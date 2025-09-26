
from fastapi import APIRouter

from app.config import get_async_database_url

user_router = APIRouter(
    tags=['User']
)

@user_router.post('/users/login')
async def login_proc(
):
    return get_async_database_url()