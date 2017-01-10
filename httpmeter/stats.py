import sys
import time
from typing import Dict, List, Any, Iterable


class Progress:
    """Displays responses progress."""

    def __init__(self) -> None:
        self._last_flushed = 0
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


class BenchmarkResults:
    def __init__(self, min_doc_len: int, avg_doc_len: int, max_doc_len: int,
                 concurrency: int, completed_requests: int, reqs_per_sec: int,
                 min_conn_time: int, avg_conn_time: int, max_conn_time: int,
                 status_codes: Dict[str, int]) -> None:
        self.min_doc_len = min_doc_len
        self.avg_doc_len = avg_doc_len
        self.max_doc_len = max_doc_len
        self.concurrency = concurrency
        self.completed_requests = completed_requests
        self.reqs_per_sec = reqs_per_sec
        self.min_conn_time = min_conn_time
        self.avg_conn_time = avg_conn_time
        self.max_conn_time = max_conn_time
        self.status_codes = status_codes


def make_benchmark_results(stats: List['RequestStats'], duration: float,
                           concurrency: int) -> BenchmarkResults:
    status_codes = {}
    size = []
    time = []
    completed_results = len(stats)

    for entry in stats:
        size.append(entry.content_size)
        time.append(entry.duration)
        inc(status_codes, entry.status_code)

    return BenchmarkResults(
            min(size), avg(size), max(size), concurrency, completed_results,
            completed_results / duration,
            min(time), avg(time), max(time), status_codes)


def results_to_str(stats: list, duration: float, concurrency: int) -> str:
    results = make_benchmark_results(stats, duration, concurrency)
    lines = [
        'Concurrency Level:        %d' % (results.concurrency),
        'Completed Requests:       %d' % (results.completed_requests),
        'Requests Per Second:      %f [#/sec] (mean)' % (results.reqs_per_sec),
        'Connection Times Total:   [min: %f, avg: %f, max: %f] seconds'
        % (results.min_conn_time, results.avg_conn_time,
           results.max_conn_time),
        'Document Length:          [min: %d, avg: %f, max: %d] bytes'
        % (results.min_doc_len, results.avg_doc_len, results.max_doc_len),
        'Status codes:',
    ]
    for status_code, count in results.status_codes.items():
        lines.append('\t%s %d' % (status_code, count))

    return '\n'.join(lines)


def inc(assoc_arr: dict, key: Any) -> None:
    """Increase by one or initialize value in associative array."""
    assoc_arr[key] = assoc_arr.get(key, 0) + 1


def avg(iter: Iterable) -> float:
    return sum(iter) / len(iter)
