import sys
import time
from typing import List
import multiprocessing
import itertools
import functools

from . import net, cli, stats, utils


class Benchmark:
    """Benchmark is used to execute performance tests and collect results."""

    def __init__(self, config, progress=None, loop=None) -> None:
        self._conf = config
        self._progress = progress

        self.stats = []
        self.requests = net.HttpRequests(loop)\
            .on_response(self._on_response)\
            .with_headers(config.headers)\
            .via_proxy(config.proxy)

    def run(self) -> List[stats.ForRequest]:
        """Executes benchmark."""
        self.requests.exec_to(self._conf.url, self._conf.concurrency,
                              self._conf.requests)
        return self.stats

    def _on_response(self, resp_text: str, status_code: int,
                     request_start_time: float) -> None:
        self.stats.append(stats.ForRequest(
            len(resp_text),
            status_code,
            time.time() - request_start_time
        ))

        if self._progress:
            self._progress.update('.')


def make_requests(conf, progress, loop) -> List[stats.ForRequest]:
    return Benchmark(conf, progress, loop).run()


def main(args: list=sys.argv[1:]) -> None:
    conf = cli.parse_args(args)
    if conf.use_uvloop:
        net.use_uvloop()

    progress = stats.Progress()

    process_count = multiprocessing.cpu_count()
    proc_pool = multiprocessing.Pool(processes=process_count)
    proc_stats, duration = utils.time_it(lambda: proc_pool.map(
        functools.partial(make_requests, conf, progress),
        net.make_event_loops(process_count),
    ))
    proc_pool.close()
    proc_pool.join()

    progress.done()

    requests_stats = list(itertools.chain.from_iterable(proc_stats))
    bench_results = stats.ForBenchmark(requests_stats, conf.concurrency,
                                       duration).summary()
    print(stats.results_to_str(bench_results))


if __name__ == '__main__':
    main()
