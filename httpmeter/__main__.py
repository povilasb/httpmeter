import sys
import time
from typing import List, Tuple
import multiprocessing
import itertools
import functools

from . import net, cli, stats, utils


class Benchmark:
    """Benchmark is used to execute performance tests and collect results."""

    def __init__(self, config, progress=None) -> None:
        self._conf = config
        self._progress = progress

        self.stats: List[stats.ForRequest] = []
        self.requests = net.HttpRequests()\
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
    return Benchmark(conf, progress).run()


def requests_per_process(process_count: int, conf) -> Tuple[int, int]:
    """Divides how many requests each forked process will make."""
    return (
        int(conf.concurrency / process_count),
        int(conf.requests / process_count),
    )


def main(args: list=sys.argv[1:]) -> None:
    conf = cli.parse_args(args)
    if conf.use_uvloop:
        net.use_uvloop()

    conf.concurrency, conf.requests = requests_per_process(
        conf.process_count, conf)
    proc_pool = multiprocessing.Pool(processes=conf.process_count)

    progress = stats.Progress()
    proc_stats, duration = utils.time_it(lambda: proc_pool.map(
        functools.partial(make_requests, conf, progress),
        range(conf.process_count)
    ))
    proc_pool.close()
    proc_pool.join()

    progress.done()

    requests_stats = list(itertools.chain.from_iterable(proc_stats))
    bench_results = stats.ForBenchmark(
        requests_stats, conf.concurrency * conf.process_count,
        duration).summary()
    print(stats.results_to_str(bench_results))


if __name__ == '__main__':
    main()
