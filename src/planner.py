from dataclasses import dataclass
from typing import List

from .graph import WeightedGraph
from .knapsack import zero_one_knapsack
from .models import Parcel, PackingResult, RouteResult
from .sorting import merge_sort_parcels
from .tsp import nearest_neighbor_tsp


@dataclass
class PlannerResult:
    sorted_parcels: List[Parcel]
    packing: PackingResult
    route: RouteResult


class CourierPlanner:
    """Coordinates sorting, packing, shortest paths and route planning."""

    def __init__(self, graph: WeightedGraph, capacity: int) -> None:
        self.graph = graph
        self.capacity = capacity

    def plan(self, parcels: List[Parcel], depot: str) -> PlannerResult:
        sorted_parcels = merge_sort_parcels(parcels)
        packing = zero_one_knapsack(sorted_parcels, self.capacity)
        destinations = [parcel.destination for parcel in packing.selected_parcels]
        route = nearest_neighbor_tsp(self.graph, depot, destinations)
        return PlannerResult(
            sorted_parcels=sorted_parcels,
            packing=packing,
            route=route,
        )
