import asyncio
from unittest.mock import patch, MagicMock, ANY

from asynctest import CoroutineMock
import pytest
from hamcrest import assert_that, is_, equal_to

from httpmeter import net


def describe_HttpRequests():
    def describe_make_requests():
        def it_returns_a_list_of_request_tasks():
            reqs = net.HttpRequests()
            reqs.make_get = MagicMock(side_effect=['req1', 'req2', 'req3'])

            tasks = reqs.make_requests('example.com', 3)

            assert_that(tasks, is_(['req1', 'req2', 'req3']))

    def describe_make_get():
        def describe_when_proxy_is_set():
            @pytest.mark.asyncio
            async def it_executes_request_via_proxy():
                reqs = net.HttpRequests().via_proxy('http://localhost:8080')
                reqs._on_response = MagicMock()

                with patch('aiohttp.request', CoroutineMock()) as request:
                    await reqs.make_get('http://example.com', 0)

                    request.assert_called_with(
                        ANY, ANY, connector=ANY,
                        headers=ANY, proxy='http://localhost:8080', loop=ANY)

        def describe_when_headers_are_set():
            @pytest.mark.asyncio
            async def it_executes_request_with_specified_headers():
                reqs = net.HttpRequests().with_headers({
                    'X-Header1': 'val1', 'X-Header2': 'val2'})

                with patch('aiohttp.request', CoroutineMock()) as request:
                    await reqs.make_get('http://example.com', 0)

                    request.assert_called_with(
                        ANY, ANY, connector=ANY,
                        headers={'X-Header1': 'val1', 'X-Header2': 'val2'},
                        proxy=ANY, loop=ANY)

        @pytest.mark.asyncio
        async def it_delegates_response_handling_to_on_response():
            reqs = net.HttpRequests()
            reqs._on_response = MagicMock()

            resp = CoroutineMock(status=302)
            resp.read.return_value = 'redirected'

            with patch('aiohttp.request', CoroutineMock(return_value=resp)):
                await reqs.make_get('http://example.com', 0)

            reqs._on_response.assert_called_with('redirected', 302, ANY)

    def describe_exec_to():
        def it_executes_all_requests():
            reqs = net.HttpRequests(asyncio.new_event_loop())
            requests = [AsyncMock(), AsyncMock(), AsyncMock()]
            reqs.make_requests = MagicMock(return_value=requests)

            reqs.exec_to('example.com', 3, 3)

            assert_that(requests[0].call_count, is_(1))
            assert_that(requests[1].call_count, is_(1))
            assert_that(requests[2].call_count, is_(1))

    def describe_via_proxy():
        def it_returns_pointer_to_self_object():
            reqs = net.HttpRequests()

            new_reqs = reqs.via_proxy('localhost:8080')

            assert_that(new_reqs, equal_to(reqs))


class AsyncMock(MagicMock):

    async def __await__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)
