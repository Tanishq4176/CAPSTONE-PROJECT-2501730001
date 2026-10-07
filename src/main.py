from pathlib import Path
import csv

from .benchmark import run_benchmark
from .data_loader import load_coordinates, load_graph, load_parcels
from .planner import CourierPlanner
from .reporting import render_plan
from .visualize import plot_benchmark, plot_route


ROOT = Path(__file__).resolve().parents[1]
PARCEL_FILE = ROOT / "datasets" / "parcels.csv"
EDGE_FILE = ROOT / "datasets" / "routes.csv"
COORDINATE_FILE = ROOT / "datasets" / "locations.csv"
IMAGE_DIR = ROOT / "images"


def main() -> None:
    IMAGE_DIR.mkdir(exist_ok=True)
    parcels = load_parcels(PARCEL_FILE)
    graph = load_graph(EDGE_FILE)
    coordinates = load_coordinates(COORDINATE_FILE)

    planner = CourierPlanner(graph=graph, capacity=15)
    result = planner.plan(parcels=parcels, depot="D")

    output = render_plan(result)
    print(output)

    with open(ROOT / "sample_run.txt", "w", encoding="utf-8") as file:
        file.write(output + "\n")

    plot_route(graph, coordinates, result.route, IMAGE_DIR / "route_visualization.png")

    benchmark_results = run_benchmark()
    plot_benchmark(benchmark_results, IMAGE_DIR / "runtime_comparison.png")
    with open(ROOT / "benchmark_results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["algorithm", "input_size", "average_runtime_seconds", "average_runtime_ms"])
        for algorithm, points in benchmark_results.items():
            for size, seconds in points:
                writer.writerow([algorithm, size, f"{seconds:.10f}", f"{seconds * 1000:.4f}"])

    print("\nGenerated:")
    print("- images/route_visualization.png")
    print("- images/runtime_comparison.png")
    print("- images/runtime_sorting.png")
    print("- images/runtime_knapsack.png")
    print("- images/runtime_route_planning.png")
    print("- benchmark_results.csv")


if __name__ == "__main__":
    main()
