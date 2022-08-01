from fastapi import APIRouter, Response, status, HTTPException, Depends
from companyService.v1.schemas import Message
from busService.v1.schemas import BusRegister
from busService.v1.controllers import BusController
from companyService.v1.controllers import CompanyController
from userService.v1.models import User
from config.middlewares import is_owner
from config.deps import get_controller


busrouter = APIRouter(prefix="/bus", tags=["bus"])


@busrouter.post(
    "/register/{company_id}", response_model=Message, status_code=201
)
async def createBus(
    company_id: int,
    request: BusRegister,
    user: User = Depends(is_owner),
    busController: BusController = Depends(get_controller(BusController)),
):
    if not (company := await CompanyController.get_company_by_id(company_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no company exists"
        )
    if company.owner != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not authorized here",
        )
    if request.representative and (
        not await CompanyController.check_related(
            company_id, request.representative
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="staf doesn't belog to company",
        )
    if await busController.check_bus_by_number(request.bus_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="bus already exists"
        )

    bus_id = await busController.create_bus(
        {**request.dict(), "owner": user.id, "company": company_id}
    )
    return Message(message=f"bus successfully regitered with id {bus_id}")
