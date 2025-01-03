from typing import Any, Optional, Type
import osmnx as ox
import os
from networkx.classes.multidigraph import MultiDiGraph
from crewai_tools import BaseTool
from pydantic import BaseModel
from .schemas import RouteDistanceSchema

CITY_FILE = os.getenv("CITY_GRAPHML_FILE", "lalaguna.graphml")


class RouteDistanceTool(BaseTool):
    name: str = "RouteDistanceTool"
    description: str = (
        "A tool to find the driving route distance between an origin and a destination in a map given their coordinates."
    )
    args_schema: Type[BaseModel] = RouteDistanceSchema
    city_map: Optional[MultiDiGraph] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.city_map = ox.load_graphml(CITY_FILE)
        self.city_map = ox.routing.add_edge_speeds(self.city_map)
        self.city_map = ox.routing.add_edge_travel_times(self.city_map)

    def _run(self, *args: Any, **kwargs: Any) -> int:
        x_origin = kwargs.get("x_origin")
        y_origin = kwargs.get("y_origin")
        x_destination = kwargs.get("x_destination")
        y_destination = kwargs.get("y_destination")

        return self._find_distance(x_origin, y_origin, x_destination, y_destination)

    def _find_distance(
        self,
        x_origin: float,
        y_origin: float,
        x_destination: float,
        y_destination: float,
    ) -> int:
        origin_node = ox.distance.nearest_nodes(self.city_map, X=x_origin, Y=y_origin)
        destination_node = ox.distance.nearest_nodes(
            self.city_map, X=x_destination, Y=y_destination
        )
        route = ox.shortest_path(
            self.city_map, origin_node, destination_node, weight="travel_time"
        )
        edge_lengths = ox.routing.route_to_gdf(self.city_map, route)["length"]

        return round(sum(edge_lengths))
