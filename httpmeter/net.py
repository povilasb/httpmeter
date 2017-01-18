import asyncio
from functools import reduce
import time
from typing import Iterable, Awaitable, Dict

import aiohttp
import uvloop


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class HttpRequests:
    """Executes HTTP requests."""

    def __init__(self, loop=None) -> None:
        self._loop = loop or asyncio.get_event_loop()
        self._connector = aiohttp.TCPConnector(verify_ssl=False)
        self._proxy_url = None
        self._headers = None
        self._on_response = None

    def exec_to(self, url: str, concurrency: int,
                total_requests: int) -> None:
        for _ in range(int(total_requests / concurrency)):
            tasks = self.make_requests(url, concurrency)
            self._loop.run_until_complete(
                asyncio.gather(*tasks, loop=self._loop))

        self._connector.close()

    def via_proxy(self, proxy_url: str) -> 'HttpRequest':
        self._proxy_url = proxy_url
        return self

    def with_headers(self, headers: Dict[str, str]) -> 'HttpRequest':
        self._headers = headers
        return self

    def on_response(self, cb) -> 'HttpRequest':
        self._on_response = cb
        return self

    def make_requests(self, url: str, count: int) -> Iterable[Awaitable]:
        return reduce(lambda reqs, _: reqs + [self.make_get(url, time.time())],
                      range(count), [])

    async def make_get(self, url: str, start_time: float) -> Awaitable:
        resp = await aiohttp.request(
            'GET', url, connector=self._connector, proxy=self._proxy_url,
            headers=self._headers)
        text = await resp.read()
        if self._on_response:
            self._on_response(text, resp.status, start_time)
