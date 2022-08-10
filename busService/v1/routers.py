from fastapi import (
    APIRouter,
    Response,
    status,
    HTTPException,
    Depends,
    WebSocket,
)
from companyService.v1.schemas import Message
from busService.v1.schemas import BusRegister, TripRegister
from busService.v1.controllers import BusController, TripController
from companyService.v1.controllers import CompanyController
from userService.v1.models import User
from config.middlewares import (
    is_owner,
    is_owner_or_driver,
    is_driver,
    is_authenticated,
)
from config.deps import get_controller
from busService.v1.socket_manager import socketManager
from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState
import json


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


@busrouter.post(
    "/trip/create/{bus_id}", response_model=Message, status_code=201
)
async def createTrip(
    bus_id: int,
    request: TripRegister,
    user: User = Depends(is_owner_or_driver),
    tripController: TripController = Depends(get_controller(TripController)),
):
    if not (bus := BusController.get_bus_by_id(bus_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no bus exists"
        )
    if bus.owner != user.id or bus.representative != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not allowed here"
        )
    if not request.driver:
        request.driver = user.id
    trip = tripController.create_trip(**request.dict())
    return Message(message=f"bus successfully regitered with id {trip}")


@busrouter.post(
    "/trip/start/{trip_id}", response_model=Message, status_code=200
)
async def startTrip(
    trip_id: int,
    user: User = Depends(is_driver),
    tripController: TripController = Depends(get_controller(TripController)),
):
    if not (trip := tripController.get_trip_by_id(trip_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no bus exists"
        )
    if trip.driver != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not allowed here"
        )
    await tripController.change_trip_status(trip_id)
    point = "POINT(27.700769,85.300140)"
    await tripController.create_tracking(
        {
            "bus": trip.bus,
            "lattitude": 27.700769,
            "longitide": 85.300140,
            "location": point,
        }
    )

    return Message(message=f"bus successfully regitered with id {trip}")


"""
@busrouter.websocket_route("/live/{bus_id}")
async def track_bus(websocket: WebSocket,
 bus_id: int,
 user: User = Depends(is_owner_or_driver)):
   await socketManager.connect(websocket,bus_id)
   while True:
            try:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                if "type" in message_data and message_data["type"] == "dismissal":
                    await socketManager.disconnect(websocket,bus_id)
                    break
                await socketManager.broadcast(data)
            except WebSocketDisconnect:
                await socketManager.disconnect(websocket,bus_id)





@busrouter.websocket_route("/test/{bus_id}")
async def track_bus(websocket: WebSocket,
 bus_id: str):
   await socketManager.connect(websocket,bus_id)
   while True:
            try:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                print(message_data)
                #if "type" in message_data and message_data["type"] == "dismissal":
                #    await socketManager.disconnect(websocket,bus_id)
                #   break
                await TripController.create_bus_route({**message_data,"bus_id":bus_id})

                await socketManager.broadcast(data)
            except WebSocketDisconnect as e:
                 print(e)
                 await socketManager.disconnect(websocket,bus_id)


          """
