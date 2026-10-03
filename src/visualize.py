from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt

from .models import RouteResult
from .graph import WeightedGraph


def plot_route(
    graph: WeightedGraph,
    coordinates: Dict[str, Tuple[float, float]],
    route: RouteResult,
    output_path: str | Path,
) -> None:
    """Create a clean monochrome route visualisation."""
    fig, ax = plt.subplots(figsize=(10, 7))

    drawn = set()
    for source, neighbors in graph.adj.items():
        for target, _ in neighbors:
            key = tuple(sorted((source, target)))
            if key in drawn or source not in coordinates or target not in coordinates:
                continue
            drawn.add(key)
            x1, y1 = coordinates[source]
            x2, y2 = coordinates[target]
            ax.plot([x1, x2], [y1, y2], color="0.78", linewidth=1)

    for a, b in zip(route.route, route.route[1:]):
        if a in coordinates and b in coordinates:
            x1, y1 = coordinates[a]
            x2, y2 = coordinates[b]
            ax.plot([x1, x2], [y1, y2], color="black", linewidth=2.8)

    for node, (x, y) in coordinates.items():
        ax.scatter(
            [x], [y], s=70, facecolors="white", edgecolors="black", linewidths=1.2, zorder=3
        )
        ax.text(x + 0.12, y + 0.12, node, fontsize=9, color="black")

    ax.set_title("Mini-Courier Planner - Delivery Route")
    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")
    ax.grid(color="0.90", linewidth=0.7)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_benchmark(results, output_path: str | Path) -> None:
    """Create one clear runtime chart per major algorithm."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    for label, points in results.items():
        x = [item[0] for item in points]
        y = [item[1] * 1000 for item in points]
        fig, ax = plt.subplots(figsize=(9, 5.5))
        ax.plot(x, y, marker="o", linewidth=1.8, color="black")
        ax.set_title(f"Runtime - {label.replace('_', ' ').title()}")
        ax.set_xlabel("Input size")
        ax.set_ylabel("Average runtime (ms)")
        ax.grid(color="0.90", linewidth=0.7)
        fig.tight_layout()
        fig.savefig(output_path.parent / f"runtime_{label}.png", dpi=180)
        plt.close(fig)

    # Overview figure for the report. Each algorithm keeps its own x-axis scale.
    fig, axes = plt.subplots(1, len(results), figsize=(16, 5.5))
    if len(results) == 1:
        axes = [axes]
    for ax, (label, points) in zip(axes, results.items()):
        x = [item[0] for item in points]
        y = [item[1] * 1000 for item in points]
        ax.plot(x, y, marker="o", linewidth=1.8, color="black")
        ax.set_title(label.replace("_", " ").title())
        ax.set_xlabel("Input size")
        ax.set_ylabel("ms")
        ax.grid(color="0.90", linewidth=0.7)
    fig.suptitle("Runtime Comparison Across Major Modules")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
