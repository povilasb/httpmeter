import sys
import time
from typing import List
import multiprocessing
import itertools
import functools

from . import net, cli, stats, utils


class Benchmark:
    """Benchmark is used to execute performance tests and collect results."""

    def __init__(self, config, loop=None) -> None:
        self._conf = config

        self.stats = []
        self.progress = stats.Progress()
        self.requests = net.HttpRequests(loop)\
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


def make_requests(conf, loop) -> List[stats.ForRequest]:
    return Benchmark(conf, loop).run()


def main(args: list=sys.argv[1:]) -> None:
    conf = cli.parse_args(args)
    if conf.use_uvloop:
        net.use_uvloop()

    process_count = multiprocessing.cpu_count()
    proc_pool = multiprocessing.Pool(processes=process_count)
    proc_stats, duration = utils.time_it(lambda: proc_pool.map(
        functools.partial(make_requests, conf),
        net.make_event_loops(process_count),
    ))

    requests_stats = list(itertools.chain.from_iterable(proc_stats))
    bench_results = stats.ForBenchmark(requests_stats, conf.concurrency,
                                       duration).summary()
    print(stats.results_to_str(bench_results))


if __name__ == '__main__':
    main()
