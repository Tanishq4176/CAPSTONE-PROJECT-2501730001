from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass(frozen=True)
class Parcel:
    parcel_id: str
    destination: str
    weight: int
    priority: int
    deadline: int
    value: int


@dataclass
class PackingResult:
    selected_parcels: List[Parcel]
    total_weight: int
    total_value: int
    capacity: int
    dp_table: List[List[int]]


@dataclass
class ShortestPathResult:
    distance: float
    path: List[str]


@dataclass
class RouteResult:
    route: List[str]
    visit_order: List[str]
    distance: float
    legs: List[ShortestPathResult]
