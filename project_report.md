# Mini-Courier Planner
## Capstone Project Report

### 1. Abstract

Mini-Courier Planner is a Python prototype that models the planning stage of a courier delivery operation. The system combines four core algorithmic techniques: merge sort for parcel prioritization, 0/1 Knapsack dynamic programming for vehicle loading, Dijkstra's shortest-path algorithm for point-to-point routing, and nearest-neighbor TSP approximation for the overall delivery sequence. A benchmarking module records execution times on progressively larger inputs, while Matplotlib is used to generate route and runtime visualisations.

### 2. Problem statement

A courier vehicle starts at a depot with limited carrying capacity. A collection of parcels is waiting for delivery to different customer locations. Parcels have different priorities, deadlines, weights, and values. The planner must first identify which parcels deserve attention, choose a feasible set of parcels for the current trip, and then plan an efficient route through their delivery points.

The capstone objective is not simply to solve one isolated algorithmic problem. It is to integrate several algorithmic paradigms into one executable application and evaluate their performance.

### 3. Requirements derived from the capstone

The implementation provides the following required functions:

- Parcel prioritization by priority and deadline.
- Optimal package selection under a fixed vehicle capacity using dynamic programming.
- Customer graph representation using weighted adjacency lists.
- Dijkstra shortest paths for delivery legs.
- Nearest-neighbor TSP approximation for an overall tour.
- Small and larger benchmark datasets generated reproducibly.
- Runtime chart and route visualisation.
- Modular source code, dataset files, README, notebook, tests, and documentation.

### 4. System design

```text
                 +--------------------+
                 |   parcels.csv      |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 |  Merge Sort        |
                 | Priority + Deadline|
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 | 0/1 Knapsack DP    |
                 | Vehicle capacity   |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 | Selected delivery  |
                 | destinations       |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 | Dijkstra           |
                 | Shortest paths     |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 | Nearest-Neighbor   |
                 | TSP Approximation   |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 | Final route +      |
                 | distance + charts  |
                 +--------------------+
```

### 5. Data design

#### Parcel record

| Field | Meaning |
|---|---|
| parcel_id | Unique parcel code |
| destination | Customer graph node |
| weight | Capacity consumed by the parcel |
| priority | Higher value means higher urgency |
| deadline | Smaller value means earlier deadline |
| value | Benefit used by Knapsack optimisation |

#### Route graph

The graph is stored as edge records in CSV format and loaded into an adjacency-list representation. The graph is undirected and all weights are non-negative, which is suitable for Dijkstra's algorithm.

### 6. Algorithm 1: Parcel prioritization

Merge sort is implemented manually instead of calling Python's built-in `sort()` so that the algorithmic work is visible and assessable. Parcels are ordered by:

1. Higher priority first.
2. Earlier deadline first when priority is equal.
3. Higher value first as a final tie-breaker.

Time complexity: `O(n log n)`.

### 7. Algorithm 2: Box filling with 0/1 Knapsack

The vehicle capacity in the sample system is 15 units. Each parcel can be selected at most once. The DP state is:

`dp[i][w] = maximum value using the first i parcels with capacity w`

For each parcel, the algorithm compares two possibilities:

- Do not select the parcel.
- Select the parcel, if its weight fits.

The larger value is stored in the table. Backtracking from `dp[n][W]` reconstructs the selected parcel list.

Time complexity: `O(nW)`.

### 8. Algorithm 3: Dijkstra shortest path

The route graph is represented with adjacency lists. Dijkstra uses a min-heap to repeatedly expand the currently closest node. A predecessor dictionary reconstructs the shortest path once the destination is reached.

Time complexity with a heap: `O((V + E) log V)`.

### 9. Algorithm 4: Nearest-neighbor TSP approximation

After packing, the planner extracts the selected delivery locations. Starting at the depot, the algorithm repeatedly computes Dijkstra distances to all unvisited destinations and chooses the nearest one. After visiting all selected destinations, it returns to the depot.

This method is fast and easy to explain, but it is a heuristic. It does not guarantee the optimal TSP tour.

### 10. Integrated execution flow

The `CourierPlanner` class coordinates the individual modules:

```text
Load parcels + graph
        |
        v
Merge-sort parcels
        |
        v
Run 0/1 Knapsack
        |
        v
Extract selected destinations
        |
        v
Run nearest-neighbor TSP
        |
        v
Each leg is solved by Dijkstra
        |
        v
Display result + save evidence
```

### 11. Sample result

Using the included sample dataset and a capacity of 15 units, the planner selects parcels `P03, P08, P04, P10, P05`, using all 15 capacity units and reaching a total packing value of 265. The nearest-neighbor route visits `C3 -> C4 -> C5 -> C8 -> C10` and returns to depot `D`, with a total shortest-path travel distance of 35.00 km. The exact console trace is stored in `sample_run.txt` and can be reproduced by running `python -m src.main`.

### 12. Performance testing

The benchmark module generates deterministic random datasets using a fixed random seed. Sorting and Knapsack are tested over parcel counts of 100, 200, 400, 800, and 1600. Route planning is tested over 5, 8, 11, 14, and 17 graph nodes.

Runtime is measured with `time.perf_counter()` and averaged across repeated runs. The resulting chart is stored as `images/runtime_comparison.png`.

Expected trend:

- Merge sort should scale close to `n log n`.
- Knapsack grows with both the number of parcels and the capacity because of its `O(nW)` table.
- Route planning grows more quickly as the number of destinations increases because the nearest-neighbor procedure repeatedly evaluates shortest-path queries.

Actual machine-dependent timings are intentionally generated at execution time rather than hard-coded into the source.

### 13. Testing

Unit tests cover:

- Correct priority ordering.
- Knapsack capacity constraint and sample optimal value.
- A known Dijkstra shortest distance from the depot to a customer.
- Route start/end conditions and inclusion of requested destinations.

Run:

```bash
python -m unittest discover -s tests -v
```

### 14. Results and evidence

The repository contains the following evidence files:

- `sample_run.txt`: reproducible console output.
- `images/console_output.png`: screenshot-style output capture.
- `images/route_visualization.png`: route graph and selected delivery tour.
- `images/runtime_comparison.png`: overview runtime comparison.
- `images/runtime_sorting.png`, `images/runtime_knapsack.png`, `images/runtime_route_planning.png`: individual runtime charts.
- `mini_courier_planner.ipynb`: complete notebook implementation and demonstration.

### 15. Limitations

The project uses a synthetic graph and a single vehicle. Parcel deadlines influence priority order but are not modelled as a full time-window constraint. The route planner is approximate and does not search the complete TSP solution space. Real road traffic and live travel-time data are outside the scope of the assignment prototype.

### 16. Future scope

Possible extensions include multiple courier vehicles, capacity constraints in kilograms rather than abstract units, time-window scheduling, route re-planning after traffic changes, real map APIs, and comparison against stronger TSP heuristics or exact methods on small graphs.

### 17. Conclusion

Mini-Courier Planner demonstrates how sorting, dynamic programming, graph algorithms, and approximation can be integrated into a single practical software system. The modular design keeps each algorithm independently testable while the planner class connects them into one courier workflow. Performance measurement and visual evidence complete the project and make the implementation suitable for demonstration and viva discussion.
