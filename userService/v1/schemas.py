from pydantic import BaseModel


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    mobile_number: str
    category: str


class UserSignup(BaseUser):
    password: str


class UserResponse(BaseUser):
    id: int


class AuthToken(BaseModel):
    access_token: str
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str


class UserLogin(BaseModel):
    mobile_number: str
    password: str
