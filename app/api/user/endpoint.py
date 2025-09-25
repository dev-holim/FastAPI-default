
from fastapi import APIRouter

user_router = APIRouter(
    tags=['User']
)

@user_router.post('/users/login')
async def login_proc(
):
    ...