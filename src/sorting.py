from typing import List
from .models import Parcel


def merge_sort_parcels(parcels: List[Parcel]) -> List[Parcel]:
    """Sort parcels by priority (high first), then deadline (early first).

    Merge sort is stable and runs in O(n log n) time.
    """
    if len(parcels) <= 1:
        return parcels.copy()

    mid = len(parcels) // 2
    left = merge_sort_parcels(parcels[:mid])
    right = merge_sort_parcels(parcels[mid:])

    result: List[Parcel] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if _sort_key(left[i]) <= _sort_key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def _sort_key(parcel: Parcel):
    # Negative priority gives descending priority while deadline stays ascending.
    return (-parcel.priority, parcel.deadline, -parcel.value)
