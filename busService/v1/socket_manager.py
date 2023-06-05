from fastapi import WebSocket, WebSocketDisconnect, BackgroundTasks
import json
from typing import List, Dict
from busService.v1.controllers import BusLocationController


class BusConnection:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.owner = ""

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await websocket.close()

    async def broadcast(self, me, data):
        for websocket in self.active_connections:
            if me == 0 or websocket is not me:
                await websocket.send_json(data)


class SocketManager:
    def __init__(self):
        self.bus_list: Dict[str, BusConnection] = {}

    async def connect(self, websocket: WebSocket, id: str):
        if id in self.bus_list:
            await self.bus_list[id].connect(websocket)
        else:
            self.bus_list[id] = BusConnection()
            await self.bus_list[id].connect(websocket)

    async def disconnect(self, websocket: WebSocket, id: str):
        await self.bus_list[id].disconnect(websocket)

    async def broadcast(self, id, me, data):
        await self.bus_list[id].broadcast(me, data)

    async def close_all(self, id: str):
        for websocket in self.bus_list[id].active_connections:
            await websocket.close()
        del self.bus_list[id]


socketManager = SocketManager()


async def relay_data(websocket: WebSocket, bus_id: int, is_bus: bool):
    await socketManager.connect(websocket, bus_id)
    while True:
        try:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            task = message_data["task"]
            if not is_bus:

                if task == "dismissal":
                    await socketManager.disconnect(websocket, bus_id)
                    break

            else:

                controller = BusLocationController()

                if task == "endtrip":
                    await controller.delete_bus_location(bus_id)
                    await socketManager.close_all(bus_id)
                    break

                if task == "insertorupdatelocation":
                    location = f'POINT({message_data["longitude"]} {message_data["latitude"]})'
                    message_data.pop("task")
                    if not (await controller.check_bus_location(bus_id)):
                        await controller.create_bus_location(
                            {
                                **message_data,
                                "bus": bus_id,
                                "location": location,
                            }
                        )
                    else:
                        await controller.update_bus_location(
                            {**message_data, "location": location}, bus_id
                        )
                    await controller.create_bus_history(
                        {**message_data, "bus": bus_id, "location": location}
                    )

                    await socketManager.broadcast(bus_id, websocket, data)

        except WebSocketDisconnect as e:
            print(e)
            await socketManager.disconnect(websocket, bus_id)
            break
