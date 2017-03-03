import sys
import time
from typing import Dict, List, Any, Iterable, Tuple
from functools import reduce
from itertools import tee

from . import utils


class ForRequest:
    """Stats for single request."""

    def __init__(self, content_size: int, status_code: int,
                 duration: float) -> None:
        self.content_size = content_size
        self.status_code = status_code
        self.duration = duration

    def __str__(self) -> str:
        return str((self.duration, self.content_size, self.status_code))

    __repr__ = __str__


class BenchmarkResults:
    def __init__(self, min_doc_len: int, avg_doc_len: int, max_doc_len: int,
                 concurrency: int, completed_requests: int, reqs_per_sec:
                 float, min_req_time: int, avg_req_time: int, max_req_time:
                 int, status_codes: Dict[int, int]) -> None:
        self.min_doc_len = min_doc_len
        self.avg_doc_len = avg_doc_len
        self.max_doc_len = max_doc_len
        self.concurrency = concurrency
        self.completed_requests = completed_requests
        self.reqs_per_sec = reqs_per_sec
        self.min_req_time = min_req_time
        self.avg_req_time = avg_req_time
        self.max_req_time = max_req_time
        self.status_codes = status_codes


def min_avg_max(iter_: Iterable[float]) -> Tuple[float, float, float]:
    it1, it2, it3 = tee(iter_, 3)
    return min(it1), utils.avg(it2), max(it3)


class ForBenchmark:
    """Stats for whole benchmark."""

    def __init__(self, stats: List[ForRequest], concurrency: int=1,
                 total_duration: float=1) -> None:
        self.stats = stats
        self.concurrency = concurrency
        self.duration = total_duration

    def content_sizes(self) -> Iterable[int]:
        return map(lambda entry: entry.content_size, self.stats)

    def durations(self) -> Iterable[float]:
        return map(lambda entry: entry.duration, self.stats)

    def status_codes(self) -> Dict[int, int]:
        return reduce(lambda codes, entry: inc(codes, entry.status_code),
                      self.stats, {})

    def completed_requests(self) -> int:
        return len(self.stats)

    def summary(self) -> BenchmarkResults:
        return BenchmarkResults(
            *min_avg_max(self.content_sizes()),
            self.concurrency, self.completed_requests(),
            self.completed_requests() / self.duration,
            *min_avg_max(self.durations()),
            self.status_codes()
        )


class Progress:
    """Displays responses progress."""

    def __init__(self) -> None:
        self._last_flushed = 0.0
        self._flush_interval = 0.2

    def update(self, status: str) -> None:
        sys.stdout.write(status)
        if self.we_should_flush():
            sys.stdout.flush()
            self._last_flushed = time.time()

    def done(self) -> None:
        sys.stdout.write('\n')
        sys.stdout.flush()

    def we_should_flush(self) -> bool:
        return time.time() > (self._last_flushed + self._flush_interval)


def results_to_str(results: BenchmarkResults) -> str:
    lines = [
        'Concurrency Level:        %d' % (results.concurrency),
        'Completed Requests:       %d' % (results.completed_requests),
        'Requests Per Second:      %f [#/sec] (mean)' % (results.reqs_per_sec),
        'Request Durations:        [min: %f, avg: %f, max: %f] seconds'
        % (results.min_req_time, results.avg_req_time,
           results.max_req_time),
        'Document Length:          [min: %d, avg: %f, max: %d] bytes'
        % (results.min_doc_len, results.avg_doc_len, results.max_doc_len),
        'Status codes:',
    ]
    for status_code, count in results.status_codes.items():
        lines.append('\t%s %d' % (status_code, count))

    return '\n'.join(lines)


def inc(assoc_arr: dict, key: Any) -> dict:
    """Increase by one or initialize value in associative array."""
    assoc_arr[key] = assoc_arr.get(key, 0) + 1
    return assoc_arr
