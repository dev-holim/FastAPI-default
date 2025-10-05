from pydantic import BaseModel

class SignUpRequest(BaseModel):
    email: str
    name: str
    password: str

class SignInRequest(BaseModel):
    email: str
    password: str