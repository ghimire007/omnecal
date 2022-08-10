from fastapi import Depends, FastAPI
from config.database import create_start_app_handler, create_stop_app_handler
from sqlalchemy.orm import Session
from typing import Dict
from userService.v1.routers import userrouter
from companyService.v1.routers import companyrouter
from busService.v1.routers import busrouter


from busService.v1.socket_manager import socketManager
from busService.v1.controllers import BusController, TripController
import json
from fastapi import WebSocket, WebSocketDisconnect


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users and authentication",
    },
    {
        "name": "company",
        "description": "Operations with companies",
    },
    {
        "name": "bus",
        "description": "Operations with bus",
    },
]


app = FastAPI()
app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))
# userService.v1.models.Base.metadata.create_all(Engine)


app.include_router(userrouter, prefix="/api/v1")
app.include_router(companyrouter, prefix="/api/v1")
app.include_router(busrouter, prefix="/api/v1")


@app.get("/")
async def root(db: Session = Depends()) -> Dict:
    return {"message": "Hello Tom"}


@app.websocket("/test/ws/{bus_id}")
async def track_bus(websocket: WebSocket, bus_id: int):
    print("here")
    await socketManager.connect(websocket, bus_id)
    while True:
        try:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            print(message_data)
            await TripController.create_bus_route(
                {**message_data, "bus_id": bus_id}
            )

            await socketManager.broadcast(data)
        except WebSocketDisconnect as e:
            print(e)
            await socketManager.disconnect(websocket, bus_id)
