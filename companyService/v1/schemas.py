from pydantic import BaseModel


class Message(BaseModel):
    message: str


class CompanyRegister(BaseModel):
    name: str
    address: str
