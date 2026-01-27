from __future__ import annotations

import os
from collections.abc import Iterable, Sequence
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def resolve_workers(workers: int | str, reserve: int = 1) -> int:
    if workers != "auto":
        return max(1, int(workers))
    # Use all available CPUs for maximum parallelization
    return max(1, os.cpu_count() or 2)


def default_chunksize(total: int, workers: int) -> int:
    if total <= 0 or workers <= 1:
        return 1
    # Larger chunks reduce overhead, optimal is 2-8x workers
    return max(1, total // (workers * 2))


def process_map(
    func: Callable[[T], R],
    items: Sequence[T] | Iterable[T],
    workers: int,
    chunksize: int | None = None,
) -> list[R]:
    if workers <= 1:
        return [func(item) for item in items]
    if chunksize is None:
        total = len(items) if isinstance(items, Sequence) else 0
        chunksize = default_chunksize(total, workers)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(func, items, chunksize=chunksize))
