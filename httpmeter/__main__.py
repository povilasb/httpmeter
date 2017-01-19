import sys
import time
from typing import List

from . import net, cli, stats


class Benchmark:
    """Benchmark is used to execute performance tests and collect results."""

    def __init__(self, config) -> None:
        self._conf = config

        self.stats = []
        self.progress = stats.Progress()
        self.requests = net.HttpRequests()\
            .on_response(self._on_response)\
            .with_headers(config.headers)\
            .via_proxy(config.proxy)

    def run(self) -> List[stats.ForRequest]:
        """Executes benchmark."""
        self.requests.exec_to(self._conf.url, self._conf.concurrency,
                              self._conf.requests)
        self.progress.done()
        return self.stats

    def _on_response(self, resp_text: str, status_code: int,
                     request_start_time: float) -> None:
        self.stats.append(stats.ForRequest(
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

    requests_stats, duration = time_it(Benchmark(conf).run)
    bench_results = stats.ForBenchmark(requests_stats, conf.concurrency,
                                       duration).summary()
    print(stats.results_to_str(bench_results))


if __name__ == '__main__':
    main(sys.argv[1:])
