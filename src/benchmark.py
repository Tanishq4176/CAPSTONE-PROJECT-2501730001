import random
import time
from typing import Callable, Dict, List, Tuple

from .graph import WeightedGraph
from .knapsack import zero_one_knapsack
from .models import Parcel
from .sorting import merge_sort_parcels
from .tsp import nearest_neighbor_tsp


def _make_parcels(size: int) -> List[Parcel]:
    parcels = []
    for i in range(size):
        parcels.append(
            Parcel(
                parcel_id=f"P{i+1}",
                destination=f"C{(i % 25) + 1}",
                weight=random.randint(1, 5),
                priority=random.randint(1, 10),
                deadline=random.randint(1, 20),
                value=random.randint(20, 100),
            )
        )
    return parcels


def _make_graph(nodes: int) -> Tuple[WeightedGraph, str, List[str]]:
    graph = WeightedGraph()
    node_names = [f"C{i}" for i in range(nodes)]
    for i in range(nodes - 1):
        graph.add_edge(node_names[i], node_names[i + 1], 1 + (i % 7))
    # A few shortcuts reduce the graph's path length and make Dijkstra useful.
    for i in range(0, nodes - 3, 3):
        graph.add_edge(node_names[i], node_names[i + 3], 2.5)
    return graph, node_names[0], node_names[1:]


def _average_time(operation: Callable[[], None], repeats: int = 7) -> float:
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        operation()
        times.append(time.perf_counter() - start)
    return sum(times) / repeats


def run_benchmark() -> Dict[str, List[Tuple[int, float]]]:
    random.seed(42)
    results: Dict[str, List[Tuple[int, float]]] = {
        "sorting": [],
        "knapsack": [],
        "route_planning": [],
    }

    for size in [100, 200, 400, 800, 1600]:
        parcels = _make_parcels(size)
        results["sorting"].append((size, _average_time(lambda: merge_sort_parcels(parcels))))
        capacity = max(30, size // 2)
        results["knapsack"].append((size, _average_time(lambda: zero_one_knapsack(parcels, capacity))))

    for size in [5, 8, 11, 14, 17]:
        graph, depot, destinations = _make_graph(size)
        results["route_planning"].append(
            (size, _average_time(lambda: nearest_neighbor_tsp(graph, depot, destinations)))
        )

    return results
