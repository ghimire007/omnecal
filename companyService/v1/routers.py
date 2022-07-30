from fastapi import APIRouter, Response, status, HTTPException
from companyService.v1.schemas import CompanyRegister, Message
from userService.v1.controllers import User
from config.config import AuthJWT
from fastapi import Depends
from config.middlewares import is_owner

"""'
companyrouter = APIRouter(prefix="/company", tags=["company"])

@companyrouter.post("/register", response_model=Message, status_code=201,dependencies=[Depends(is_owner)])
async def createCompany(request: CompanyRegister, response: Response):
"""
