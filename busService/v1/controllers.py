from userService.v1.models import User
from companyService.v1.models import Company
from busService.v1.models import (
    Bus,
    Trip,
    BusLocation,
    BusTrackingHistory,
    Route,
    BusStops,
)
from config.database import database
from typing import Dict
from sqlalchemy.sql.expression import exists, select, insert, update, delete
from config.config import AuthJWT
from shapely.geometry import asShape, LineString
from geoalchemy2 import comparator, func
from geoalchemy2.shape import to_shape, from_shape
from geoalchemy2.comparator import Comparator
from sqlalchemy import and_
import polyline


class BusController:
    async def create_bus(self, bus: Dict):
        query = insert(Bus).values(**bus)
        return await database.execute(query)

    @staticmethod
    async def check_bus_by_number(number: str) -> bool:
        query = select(Bus).where(Bus.bus_number == number)
        return await database.execute(select(exists(query)))

    @staticmethod
    async def get_bus_by_id(id: int) -> Bus:
        query = select(Bus).where(Bus.id == id)
        return await database.fetch_one(query)

    async def update_bus(self, id: int, data: Dict) -> Bus:
        query = update(Bus).values(data).where(Bus.id == id)
        return await database.execute(query)

    def create_bus_token(
        self, TokenHandler: AuthJWT, bus_id: int, bus_number: str
    ) -> str:
        return TokenHandler.create_access_token(
            subject=f"{bus_id}__{bus_number}", expires_time=5000 * 24 * 60 * 60
        )


class TripController:
    async def create_trip(self, bus: Dict):
        query = insert(Trip).values(**bus)
        return await database.execute(query)

    async def create_tracking(self, tracking: Dict):
        query = insert(Trip).values(**tracking)
        return await database.execute(query)

    @staticmethod
    async def check_trip_by_id(number: str) -> bool:
        query = select(Trip).where(Trip.id == id)
        return await database.execute(select(exists(query)))

    @staticmethod
    async def get_trip_by_id(id: int) -> Trip:
        query = select(Trip).where(Trip.id == id)
        return await database.fetch_one(query)

    async def change_trip_status(self, id: int, status: str = "active") -> bool:
        query = update(Trip).values({"status": status}).where(Trip.id == id)
        return await database.execute(query)


class BusLocationController:
    async def create_bus_location(self, data: Dict):
        query = insert(BusLocation).values(**data)
        return await database.execute(query)

    async def check_bus_location(self, bus_id: int):
        query = select(BusLocation).where(BusLocation.bus == bus_id)
        return await database.execute(select(exists(query)))

    async def update_bus_location(self, data: Dict, bus_id: int):
        query = (
            update(BusLocation).values(data).where(BusLocation.bus == bus_id)
        )
        return await database.execute(query)

    async def delete_bus_location(self, bus_id: int):
        query = delete(BusLocation).where(BusLocation.bus == bus_id)
        return await database.execute(query)

    async def create_bus_history(self, data: Dict):
        query = insert(BusTrackingHistory).values(**data)
        return await database.execute(query)

    async def insert_or_update_bus_location(
        self, message_data: Dict, bus_id: int
    ):
        async with database.transaction():
            location = (
                f'POINT({message_data["longitude"]} {message_data["latitude"]})'
            )
            if not (await self.check_bus_location(bus_id)):
                await self.create_bus_location(
                    {
                        **message_data,
                        "bus": bus_id,
                        "location": location,
                    }
                )
            else:
                await self.update_bus_location(
                    {**message_data, "location": location}, bus_id
                )
            await self.create_bus_history(
                {**message_data, "bus": bus_id, "location": location}
            )


class RouteController:
    async def create_route(self, route):
        # geojson_geom = geojson.loads(json.dumps(route["route"]))
        # route["route"]= from_shape(Polygon(geojson_geom))
        # route["route"]= from_shape(Polygon(route["route"]["coordinates"][0]))
        route["route"] = from_shape(
            LineString(route["meta_data"]["coordinates"])
        )
        query = insert(Route).values(**route)
        return await database.execute(query)

    async def get_closest_busstop(self, lat: float, lon: float):
        # point=WKTElement('POINT({} {})'.format(lon, lat),srid=4326)
        point = "POINT({} {})".format(lon, lat)
        query = (
            select(BusStops)
            .order_by(
                Comparator.distance_centroid(
                    BusStops.location, func.Geometry(point)
                )
            )
            .limit(1)
        )
        """
        query=select(BusStops).order_by(
        func.ST_Distance(BusStops.location,
                     func.Geometry(func.ST_GeographyFromText(
                         'POINT({} {})'.format(lon, lat))))).limit(1)

                         query = session.query(Lake).filter(
                        func.ST_Contains(Lake.geom, 'POINT(4 1)'))
                        WKTElement('POINT(1 1)', srid=4326)
        """

        return await database.fetch_one(query)

    async def get_route_with_cordinates(self, point1, point2):
        return await database.fetch_all(
            select(Route.meta_data).where(
                (
                    func.ST_Distance(
                        func.ST_GeomFromEWKB(Route.route),
                        func.ST_GeomFromEWKB(point1),
                    )
                    < 2000
                )
                & (
                    func.ST_Distance(
                        func.ST_GeomFromEWKB(Route.route),
                        func.ST_GeomFromEWKB(point2),
                    )
                    < 2000
                )
            )
        )

        """query= select(Route).order_by(
                    Comparator.intersects(Route.route,
                    point1
                    ST_GeomFromEWKB
                    ))"""
        print(query)
        return
        ST_DistanceSphere
        """
        distance_box
        print(data)
        return data
        """

    async def add_bus_stops(self):
        from .d import x

        for elem in x:
            if elem["type"] == "node":
                query = insert(BusStops).values(
                    latitude=elem["lat"],
                    longitude=elem["lon"],
                    location=f'POINT({elem["lon"]} {elem["lat"]})',
                    name=elem["tags"].get("name")
                    or elem["tags"].get("highway")
                    or elem["tags"].get("name:en")
                    or elem["tags"].get("name:ne")
                    or elem["tags"].get("local_ref"),
                )
            await database.execute(query)


'''
       overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = """
        [out:json];
        area["ISO3166-1"="DE"][admin_level=2];
        (node["amenity"="biergarten"](area);
        way["amenity"="biergarten"](area);
        rel["amenity"="biergarten"](area);
        );
        out center 5;
        """
        response = requests.get(overpass_url,
                                params={'data': overpass_query})
        data = response.json()
        print(data)

        tags = {'building': True}
        buildings = ox.geometries_from_place("kathmandu", tags)
        print(buildings.head())

       '''
