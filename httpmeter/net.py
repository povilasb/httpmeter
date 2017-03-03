import asyncio
from functools import reduce
import time
from typing import Awaitable, Dict, List, Callable

import aiohttp
import uvloop


ResponseHandler = Callable[[str, int, float], None]


class HttpRequests:
    """Executes HTTP requests."""

    def __init__(self, loop=None) -> None:
        self._loop = loop or asyncio.new_event_loop()
        self._connector = aiohttp.TCPConnector(verify_ssl=False,
                                               loop=self._loop)
        self._proxy_url: str = None
        self._headers: Dict[str, str] = None
        self._on_response: ResponseHandler = None

    def exec_to(self, url: str, concurrency: int,
                total_requests: int) -> None:
        for _ in range(int(total_requests / concurrency)):
            tasks = self.make_requests(url, concurrency)
            self._loop.run_until_complete(
                asyncio.gather(*tasks, loop=self._loop))

        self._connector.close()

    def via_proxy(self, proxy_url: str) -> 'HttpRequests':
        self._proxy_url = proxy_url
        return self

    def with_headers(self, headers: Dict[str, str]) -> 'HttpRequests':
        self._headers = headers
        return self

    def on_response(self, cb: ResponseHandler) -> 'HttpRequests':
        self._on_response = cb
        return self

    def make_requests(self, url: str, count: int) -> List[Awaitable]:
        return reduce(lambda reqs, _: reqs + [self.make_get(url, time.time())],
                      range(count), [])

    async def make_get(self, url: str, start_time: float):
        resp = await aiohttp.request(
            'GET', url, connector=self._connector, proxy=self._proxy_url,
            headers=self._headers, loop=self._loop)
        text = await resp.read()
        if self._on_response:
            self._on_response(text, resp.status, start_time)


def use_uvloop() -> None:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
