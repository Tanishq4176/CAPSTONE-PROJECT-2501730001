from typing import List, Set
from .graph import WeightedGraph
from .models import RouteResult, ShortestPathResult


def nearest_neighbor_tsp(
    graph: WeightedGraph, start: str, destinations: List[str]
) -> RouteResult:
    """Approximate a delivery tour using nearest-neighbor on Dijkstra distances.

    The courier starts at `start`, visits every destination once, and returns to start.
    The method is an approximation for TSP and does not guarantee the optimal tour.
    """
    unvisited: Set[str] = set(destinations)
    unvisited.discard(start)
    current = start
    route = [start]
    visit_order = [start]
    legs: List[ShortestPathResult] = []
    total_distance = 0.0

    while unvisited:
        best_destination = None
        best_leg = None
        for destination in sorted(unvisited):
            leg = graph.dijkstra(current, destination)
            if best_leg is None or leg.distance < best_leg.distance:
                best_destination = destination
                best_leg = leg

        assert best_destination is not None and best_leg is not None
        route.extend(best_leg.path[1:])
        legs.append(best_leg)
        total_distance += best_leg.distance
        unvisited.remove(best_destination)
        visit_order.append(best_destination)
        current = best_destination

    if current != start:
        return_leg = graph.dijkstra(current, start)
        route.extend(return_leg.path[1:])
        legs.append(return_leg)
        total_distance += return_leg.distance

    visit_order.append(start)
    return RouteResult(route=route, visit_order=visit_order, distance=total_distance, legs=legs)
