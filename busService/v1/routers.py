from fastapi import APIRouter, Response, status, HTTPException, Depends, Request
from companyService.v1.schemas import Message
from busService.v1.schemas import BusRegister, TripRegister, BusLocation, Route
from busService.v1.controllers import (
    BusController,
    TripController,
    BusLocationController,
    RouteController,
)
from companyService.v1.controllers import CompanyController
from userService.v1.models import User
from config.middlewares import (
    is_owner,
    is_owner_or_driver,
    is_driver,
    is_authenticated,
    is_bus_or_authenticated,
)
from busService.v1.socket_manager import socketManager
from config.deps import get_controller
from config.config import AuthJWT
from typing import List
import requests
import polyline


busrouter = APIRouter(prefix="/bus", tags=["bus"])


@busrouter.post(
    "/register/{company_id}", response_model=Message, status_code=201
)
async def createBus(
    company_id: int,
    request: BusRegister,
    user: User = Depends(is_owner),
    TokenHandler: AuthJWT = Depends(),
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
    token = busController.create_bus_token(
        TokenHandler, bus_id, request.bus_number
    )
    print(token)
    await busController.update_bus(bus_id, {"token": token})
    return Message(message=f"bus successfully regitered ")


# replace the api token for IOT to communicate with server
@busrouter.post(
    "/token/replace/{bus_id}", response_model=Message, status_code=200
)
async def updateToken(
    bus_id: int,
    user: User = Depends(is_owner),
    TokenHandler: AuthJWT = Depends(),
    busController: BusController = Depends(get_controller(BusController)),
):
    if not (bus := busController.get_bus_by_id(bus_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no bus exists"
        )

    if not (bus.owner != user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no bus exists"
        )
    new_token = busController.create_bus_token(
        TokenHandler, bus.id, bus.bus_number
    )
    busController.update_bus(bus_id, {"token": new_token})
    return Message(message=f"token updated successfully")


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


"""
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


@busrouter.post(
    "/live/create/{bus_id}", response_model=Message, status_code=201
)
async def post_location(
    request: BusLocation,
    bus_id: int,
    busLocationController: BusLocationController = Depends(
        get_controller(BusLocationController)
    ),
):
    await busLocationController.insert_or_update_bus_location(
        request.dict(), bus_id
    )
    await socketManager.broadcast(str(bus_id), 0, request.dict())
    # return Message(message=f"bus location successfully tracked")


@busrouter.post("/route/create", response_model=Message, status_code=201)
async def post_route(
    request: Request,
    routeController: RouteController = Depends(RouteController),
):
    await routeController.create_route(await request.json())
    return Message(message=f"bus location successfully tracked")


@busrouter.get("/route/list", response_model=List[Route], status_code=200)
async def get_route(
    request: Request,
    longitude_start: float,
    latitude_start: float,
    latitude_end: float,
    longitude_end: float,
    routeController: RouteController = Depends(RouteController),
):
    nearest_stop_user = await routeController.get_closest_busstop(
        latitude_start, longitude_start
    )

    nearest_stop_destination = await routeController.get_closest_busstop(
        latitude_end, longitude_end
    )
    nearest_walk_route = f"https://maps.open-street.com/api/route/?origin={latitude_start:.6f},{longitude_start:.6f}&destination={nearest_stop_user.latitude:.6f},{nearest_stop_user.longitude:.6f}&mode=driving&key=9411f16c73a0962ebf9738261e6e25b8"
    wr1 = requests.get(nearest_walk_route).json()

    nearest_stop_route = f"https://maps.open-street.com/api/route/?origin={latitude_end:.6f},{longitude_end:.6f}&destination={nearest_stop_destination.latitude:.6f},{nearest_stop_destination.longitude:.6f}&mode=driving&key=9411f16c73a0962ebf9738261e6e25b8"
    wr2 = requests.get(nearest_stop_route).json()

    available_routes = await routeController.get_route_with_cordinates(
        nearest_stop_user.location, nearest_stop_destination.location
    )
    # d={"meta_data":available_routes[0]["meta_data"],"towards_stop":polyline.decode(wr1["polyline"]),
    # "towards_destination":polyline.decode(wr2["polyline"])}
    # available_routes[0]["meta_data"]=polyline.decode(wr1["polyline"])
    # available_routes[0]["meta_data"]=polyline.decode(wr2["polyline"])
    # return available_routes
    towards_stop = polyline.decode(wr1["polyline"], geojson=True)
    towards_stop = [
        [d[1] / 10, d[0] / 10] if d[1] < d[0] else [d[0] / 10, d[1] / 10]
        for d in towards_stop
    ]
    towards_destination = polyline.decode(wr2["polyline"], geojson=True)
    towards_destination = [
        [d[1] / 10, d[0] / 10] if d[1] < d[0] else [d[0] / 10, d[1] / 10]
        for d in towards_destination
    ]

    return [
        Route(
            meta_data=available_routes[0]["meta_data"],
            towards_stop=towards_stop,
            towards_destination=towards_destination,
        )
    ]


@busrouter.post("/busstops/create", response_model=Message, status_code=200)
async def create_ROUTE(
    request: Request,
    routeController: RouteController = Depends(RouteController),
):
    await routeController.add_bus_stops()
    return Message(message=f"bus location successfully tracked")
