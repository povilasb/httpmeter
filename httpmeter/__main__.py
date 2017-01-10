import sys
import time
from typing import List

from . import net, cli, summary


class RequestStats:

    def __init__(self, content_size: int, status_code: int,
                 duration: int) -> None:
        self.content_size = content_size
        self.status_code = status_code
        self.duration = duration

    def __str__(self) -> str:
        return str((self.duration, self.content_size, self.status_code))

    __repr__ = __str__


class Benchmark:
    """Benchmark is used to execute performance tests and collect results."""

    def __init__(self, config) -> None:
        self._conf = config

        self.stats = []
        self.progress = summary.Progress()
        self.requests = net.HttpRequests().on_response(self._on_response)

    def run(self) -> List[RequestStats]:
        """Executes benchmark."""
        self.requests.exec_to(self._conf.url, self._conf.concurrency,
                              self._conf.requests)
        self.progress.done()
        return self.stats

    def _on_response(self, resp_text: str, status_code: int,
                     request_start_time: float) -> None:
        self.stats.append(RequestStats(
            len(resp_text),
            status_code,
            time.time() - request_start_time
        ))

        self.progress.update('.')


def time_it(cb) -> float:
    start_time = time.time()
    result = cb()
    return result, time.time() - start_time


def main(args) -> None:
    conf = cli.parse_args(args)

    stats, duration = time_it(Benchmark(conf).run)
    print(summary.results_to_str(stats, duration, conf.concurrency))


if __name__ == '__main__':
    main(sys.argv[1:])
