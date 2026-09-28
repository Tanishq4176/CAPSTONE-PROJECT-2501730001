from typing import List
from .models import Parcel, PackingResult


def zero_one_knapsack(parcels: List[Parcel], capacity: int) -> PackingResult:
    """Select a maximum-value subset of parcels under a weight capacity.

    Uses 0/1 dynamic programming. Time: O(n * capacity).
    Space: O(n * capacity) so the complete DP table can be shown in the report.
    """
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        parcel = parcels[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if parcel.weight <= w:
                candidate = dp[i - 1][w - parcel.weight] + parcel.value
                if candidate > dp[i][w]:
                    dp[i][w] = candidate

    selected: List[Parcel] = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            w -= parcel.weight

    selected.reverse()
    return PackingResult(
        selected_parcels=selected,
        total_weight=sum(p.weight for p in selected),
        total_value=sum(p.value for p in selected),
        capacity=capacity,
        dp_table=dp,
    )
