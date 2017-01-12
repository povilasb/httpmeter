from itertools import tee
from typing import Iterable


def count(iter_: Iterable) -> int:
    return sum(1 for _ in iter_)


def avg(iter_: Iterable[int]) -> float:
    it1, it2 = tee(iter_)
    try:
        return sum(it1) / count(it2)
    except ZeroDivisionError:
        return 0
