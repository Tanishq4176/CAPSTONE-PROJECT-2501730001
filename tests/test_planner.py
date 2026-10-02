import unittest

from src.data_loader import load_graph, load_parcels
from src.knapsack import zero_one_knapsack
from src.sorting import merge_sort_parcels
from src.tsp import nearest_neighbor_tsp


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]


class TestMiniCourierPlanner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parcels = load_parcels(ROOT / "datasets" / "parcels.csv")
        cls.graph = load_graph(ROOT / "datasets" / "routes.csv")

    def test_sorting_prioritizes_high_priority(self):
        sorted_parcels = merge_sort_parcels(self.parcels)
        priorities = [p.priority for p in sorted_parcels]
        self.assertEqual(priorities, sorted(priorities, reverse=True))

    def test_knapsack_respects_capacity(self):
        result = zero_one_knapsack(self.parcels, 15)
        self.assertLessEqual(result.total_weight, 15)
        self.assertEqual(result.total_value, 265)

    def test_dijkstra_returns_known_shortest_path(self):
        result = self.graph.dijkstra("D", "C6")
        self.assertAlmostEqual(result.distance, 10.0)
        self.assertEqual(result.path[0], "D")
        self.assertEqual(result.path[-1], "C6")

    def test_tsp_route_visits_selected_destinations(self):
        destinations = ["C1", "C3", "C5", "C8"]
        result = nearest_neighbor_tsp(self.graph, "D", destinations)
        for destination in destinations:
            self.assertIn(destination, result.route)
        self.assertEqual(result.route[0], "D")
        self.assertEqual(result.route[-1], "D")
        self.assertEqual(result.visit_order, ["D", "C1", "C3", "C5", "C8", "D"])
        self.assertGreater(result.distance, 0)


if __name__ == "__main__":
    unittest.main()
