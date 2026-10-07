# Mini-Courier Planner

A modular Python capstone project that integrates sorting, dynamic programming, graph algorithms, approximation, performance testing, and data visualisation into a small courier-planning system.

## 1. Project objective

The planner receives a parcel dataset and a weighted delivery graph. It then:

1. Prioritizes parcels using stable merge sort.
2. Selects the best set of parcels for a delivery vehicle using 0/1 Knapsack dynamic programming.
3. Finds shortest paths between delivery locations using Dijkstra's algorithm.
4. Builds an overall delivery tour using nearest-neighbor TSP approximation.
5. Benchmarks major components on different input sizes and produces runtime charts.

The design directly follows the five capstone phases in the assignment brief: problem design, package prioritization and box filling, route/graph processing, performance testing, and final reporting/demonstration.

## 2. Technology

- Python 3.10+
- Standard library: `csv`, `heapq`, `dataclasses`, `unittest`, `time`, `random`
- Matplotlib for route and runtime visualisation
- Jupyter Notebook for the complete implementation walkthrough

No web framework or database is required for the assignment prototype. The application is intentionally focused on the algorithms assessed in the capstone.

## 3. Project structure

```text
mini_courier_planner/
├── README.md
├── mini_courier_planner.ipynb
├── requirements.txt
├── .gitignore
├── sample_run.txt
├── project_report.md
├── datasets/
│   ├── parcels.csv
│   ├── routes.csv
│   └── locations.csv
├── images/
│   ├── route_visualization.png
│   ├── runtime_comparison.png
│   └── console_output.png
├── src/
│   ├── __init__.py
│   ├── benchmark.py
│   ├── data_loader.py
│   ├── graph.py
│   ├── knapsack.py
│   ├── main.py
│   ├── models.py
│   ├── planner.py
│   ├── reporting.py
│   ├── sorting.py
│   ├── tsp.py
│   └── visualize.py
└── tests/
    └── test_planner.py
```

## 4. Dataset format

### `datasets/parcels.csv`

- `parcel_id`: unique parcel identifier
- `destination`: delivery node
- `weight`: parcel weight in capacity units
- `priority`: larger value means higher priority
- `deadline`: smaller value means earlier deadline
- `value`: benefit assigned to the parcel for the packing optimisation

### `datasets/routes.csv`

A weighted undirected graph represented as edge records:

- `source`
- `target`
- `distance`

### `datasets/locations.csv`

Two-dimensional coordinates used only to draw the route visualisation:

- `node`
- `x`
- `y`

## 5. How to run

Open a terminal in the project root.

### Windows PowerShell / Command Prompt

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m src.main
```

The program prints the complete planning result and regenerates:

- `sample_run.txt`
- `images/route_visualization.png`
- `images/runtime_comparison.png`

## 6. Run tests

```bash
python -m unittest discover -s tests -v
```

The test suite checks sorting order, knapsack capacity and expected value, a known Dijkstra result, and basic route validity.

## 7. Notebook

`mini_courier_planner.ipynb` contains the complete implementation flow in a presentation-friendly format. It loads the datasets, runs each algorithm, shows the planning result, and produces the visualisations.

## 8. Algorithm choices

### Merge sort
Used for parcel prioritization because its worst-case time complexity is `O(n log n)` and it preserves the relative order of equal keys.

### 0/1 Knapsack
Used because each parcel is either selected or not selected. Dynamic programming gives an exact solution for the small integer-capacity formulation used here.

Time complexity: `O(nW)` where `n` is the number of parcels and `W` is the vehicle capacity.

### Dijkstra
Used for shortest path queries on the non-negative weighted delivery graph.

With a binary heap and adjacency lists, the typical complexity is `O((V + E) log V)`.

### Nearest-neighbor TSP approximation
Used to generate a practical overall delivery order without solving the NP-hard TSP exactly. At each step, the nearest unvisited destination is selected according to the Dijkstra shortest-path distance.

This is a heuristic and is not guaranteed to produce the optimal tour.

## 9. Assignment mapping

| Capstone phase | Implementation evidence |
|---|---|
| Phase 1: Design and Planning | `project_report.md`, architecture, datasets, algorithm selection |
| Phase 2: Package Prioritization and Box Filling | `src/sorting.py`, `src/knapsack.py`, DP table in notebook/output |
| Phase 3: Route Maker and Graph Processing | `src/graph.py`, `src/tsp.py`, route output and image |
| Phase 4: Performance Testing and Optimization | `src/benchmark.py`, `images/runtime_comparison.png` |
| Phase 5: Final Report and Demonstration | `README.md`, `project_report.md`, screenshots, notebook |

## 10. GitHub submission

Recommended final repository name:

`mini-courier-planner`

Before submission, commit all files and tag the final commit exactly as required by the assignment:

```bash
git add .
git commit -m "Final capstone submission"
git tag v1.0-final-submission
git push origin main --tags
```

Then submit the repository URL through the LMS/Zosima portal.

## 11. Scope and limitations

This is a planning prototype rather than a production logistics platform. The TSP route is heuristic, the vehicle capacity is expressed in integer capacity units, and route coordinates are synthetic. Real traffic, time windows, multiple vehicles, and live maps can be added as future work without changing the core algorithm modules.
