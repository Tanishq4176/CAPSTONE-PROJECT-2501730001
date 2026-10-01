from pathlib import Path
from typing import Iterable

from .models import Parcel
from .planner import PlannerResult


def render_plan(result: PlannerResult) -> str:
    lines = []
    lines.append("MINI-COURIER PLANNER")
    lines.append("=" * 70)
    lines.append("Parcel prioritization")
    lines.append("-" * 70)
    lines.append("ID     Destination  Weight  Priority  Deadline  Value")
    for parcel in result.sorted_parcels:
        lines.append(
            f"{parcel.parcel_id:<6} {parcel.destination:<12} {parcel.weight:>6} "
            f"{parcel.priority:>8} {parcel.deadline:>9} {parcel.value:>6}"
        )

    packing = result.packing
    lines.append("")
    lines.append("Packing plan (0/1 Knapsack)")
    lines.append("-" * 70)
    lines.append("Selected: " + ", ".join(p.parcel_id for p in packing.selected_parcels))
    lines.append(f"Total weight : {packing.total_weight} / {packing.capacity}")
    lines.append(f"Total value  : {packing.total_value}")

    route = result.route
    lines.append("")
    lines.append("Route plan (Dijkstra + Nearest-Neighbor TSP)")
    lines.append("-" * 70)
    lines.append("Delivery order: " + " -> ".join(route.visit_order))
    lines.append("Expanded shortest-path traversal: " + " -> ".join(route.route))
    lines.append(f"Total route distance: {route.distance:.2f} km")
    lines.append("")
    lines.append("Shortest-path legs")
    for index, leg in enumerate(route.legs, start=1):
        lines.append(
            f"Leg {index}: {' -> '.join(leg.path)} ({leg.distance:.2f} km)"
        )
    return "\n".join(lines)
