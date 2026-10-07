import csv
from pathlib import Path
from typing import Dict, List, Tuple
from .graph import WeightedGraph
from .models import Parcel


def load_parcels(path: str | Path) -> List[Parcel]:
    parcels: List[Parcel] = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            parcels.append(
                Parcel(
                    parcel_id=row["parcel_id"],
                    destination=row["destination"],
                    weight=int(row["weight"]),
                    priority=int(row["priority"]),
                    deadline=int(row["deadline"]),
                    value=int(row["value"]),
                )
            )
    return parcels


def load_graph(path: str | Path) -> WeightedGraph:
    graph = WeightedGraph()
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            graph.add_edge(row["source"], row["target"], float(row["distance"]))
    return graph


def load_coordinates(path: str | Path) -> Dict[str, Tuple[float, float]]:
    coordinates: Dict[str, Tuple[float, float]] = {}
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            coordinates[row["node"]] = (float(row["x"]), float(row["y"]))
    return coordinates
