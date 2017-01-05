import asyncio
from functools import reduce
import time
from typing import Iterable, List, Awaitable

import aiohttp

from . import summary


class RequestStats:

    def __init__(self, content_size: int, status_code: int,
                 duration: int) -> None:
        self.content_size = content_size
        self.status_code = status_code
        self.duration = duration

    def __str__(self) -> str:
        return str((self.duration, self.content_size, self.status_code))

    __repr__ = __str__


class HttpRequests:
    """Executes HTTP requests."""

    def __init__(self, loop=None) -> None:
        self._verbose = False
        self._loop = loop or asyncio.get_event_loop()
        self._connector = aiohttp.TCPConnector(verify_ssl=False)
        self._stats = []
        self._proxy_url = None
        self._progress = None

    def exec_to(self, url: str, concurrency: int,
                total_requests: int) -> List[RequestStats]:
        self._stats = []

        for _ in range(int(total_requests / concurrency)):
            tasks = self.make_requests(url, concurrency)
            self._loop.run_until_complete(
                asyncio.gather(*tasks, loop=self._loop))

        self._connector.close()
        if self._progress:
            self._progress.done()

        return self._stats

    def verbose(self, value: bool) -> 'HttpRequest':
        self._verbose = value
        return self

    def via_proxy(self, proxy_url: str) -> 'HttpRequest':
        self._proxy_url = proxy_url
        return self

    def show_progress(
            self, progress_output: summary.Progress) -> 'HttpRequest':
        self._progress = progress_output
        return self

    def make_requests(self, url: str, count: int) -> Iterable[Awaitable]:
        return reduce(lambda reqs, _: reqs + [self.make_get(url, time.time())],
                      range(count), [])

    async def make_get(self, url: str, start_time: float) -> Awaitable:
        resp = await aiohttp.request('GET', url, connector=self._connector,
                                     proxy=self._proxy_url)
        text = await resp.read()
        self._on_response(text, resp.status, start_time)

    def _on_response(self, resp_text: str, status_code: int,
                     request_start_time: float) -> None:
        self._stats.append(RequestStats(
            len(resp_text),
            str(status_code),
            time.time() - request_start_time
        ))

        if self._verbose:
            print(resp_text)

        if self._progress:
            self._progress.update('.')
