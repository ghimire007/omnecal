from pydantic import BaseModel


class Message(BaseModel):
    message: str


class CompanyRegister(BaseModel):
    id: int
    name: str
    address: str
