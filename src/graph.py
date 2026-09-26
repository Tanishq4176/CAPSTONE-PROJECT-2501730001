import heapq
from typing import Dict, List, Tuple, Iterable
from .models import ShortestPathResult


class WeightedGraph:
    """Undirected weighted graph represented with adjacency lists."""

    def __init__(self) -> None:
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def add_edge(self, source: str, target: str, weight: float) -> None:
        if weight < 0:
            raise ValueError("Dijkstra requires non-negative edge weights.")
        self.adj.setdefault(source, []).append((target, weight))
        self.adj.setdefault(target, []).append((source, weight))

    def nodes(self) -> Iterable[str]:
        return self.adj.keys()

    def dijkstra(self, start: str, target: str) -> ShortestPathResult:
        """Return the shortest distance and path from start to target."""
        if start not in self.adj or target not in self.adj:
            raise KeyError(f"Unknown node: {start if start not in self.adj else target}")

        distances = {node: float("inf") for node in self.adj}
        previous = {node: None for node in self.adj}
        distances[start] = 0.0
        heap = [(0.0, start)]

        while heap:
            current_distance, node = heapq.heappop(heap)
            if current_distance != distances[node]:
                continue
            if node == target:
                break

            for neighbor, weight in self.adj[node]:
                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = node
                    heapq.heappush(heap, (new_distance, neighbor))

        if distances[target] == float("inf"):
            raise ValueError(f"No route exists between {start} and {target}.")

        path = []
        current = target
        while current is not None:
            path.append(current)
            if current == start:
                break
            current = previous[current]
        path.reverse()

        return ShortestPathResult(distance=distances[target], path=path)
