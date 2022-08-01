from fastapi import APIRouter, Response, status, HTTPException, Depends
from companyService.v1.schemas import CompanyRegister, Message
from companyService.v1.controllers import CompanyController
from userService.v1.controllers import UserController
from userService.v1.models import User
from companyService.v1.models import Company, Company_User
from config.middlewares import is_owner, is_driver
from config.deps import get_controller


companyrouter = APIRouter(prefix="/company", tags=["company"])


@companyrouter.post("/register", response_model=Message, status_code=201)
async def createCompany(
    request: CompanyRegister,
    user: User = Depends(is_owner),
    companyController: CompanyController = Depends(CompanyController),
):
    company_id = await companyController.create_company(
        {**request.dict(), "owner": user.id}
    )
    return Message(message=f"sucessfully created a company {company_id}")


@companyrouter.post(
    "/invite/accept/{company_id}", response_model=Message, status_code=200
)
async def acceptInvite(
    company_id: int,
    user: User = Depends(is_driver),
    companyController: CompanyController = Depends(CompanyController),
):
    if not (await companyController.check_invite(company_id, user.id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no invite exists"
        )
    await companyController.accept_invite(company_id, user.id)
    return Message(message=f"accepted the invitation")


@companyrouter.post(
    "/invite/{company_id}/{staff_id}", response_model=Message, status_code=201
)
async def createInvite(
    company_id: int,
    staff_id: int,
    user: User = Depends(is_owner),
    companyController: CompanyController = Depends(CompanyController),
):
    if not (
        await UserController.check_user_by_id(staff_id)
        and (company := await CompanyController.get_company_by_id(company_id))
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="either company or user is invalid",
        )
    print(await companyController.check_invite(company_id, user.id))
    if await companyController.check_invite(company_id, user.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="invite already exists"
        )
    if company.owner != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not authorized",
        )
    await companyController.invite_representative(company_id, staff_id)
    return Message(message=f"created the invitation")
