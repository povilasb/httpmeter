from unittest.mock import MagicMock, patch

from hamcrest import assert_that, is_

from httpmeter.__main__ import Benchmark


def describe_Bencmark():
    def describe_constructor():
        def it_instantiates_http_requests_with_headers_specified_in_config():
            requests = MagicMock()
            requests.on_response.return_value = requests

            with patch('httpmeter.net.HttpRequests',
                       MagicMock(return_value=requests)):
                Benchmark(MagicMock(headers={'Connection': 'close'}))

                requests.with_headers.assert_called_with({'Connection': 'close'})

        def it_instantiates_http_requests_with_proxy_specified_in_config():
            requests = MagicMock()
            requests.on_response.return_value = requests
            requests.with_headers.return_value = requests

            with patch('httpmeter.net.HttpRequests',
                       MagicMock(return_value=requests)):
                Benchmark(MagicMock(proxy='http://localhost:1080'))

                requests.via_proxy.assert_called_with('http://localhost:1080')

    def describe__on_response():
        def it_updates_progress():
            bench = Benchmark(MagicMock())
            bench.progress = MagicMock()

            bench._on_response('resp', 200, 0)

            bench.progress.update.assert_called_with('.')

        @patch('time.time', MagicMock(return_value=100))
        def it_appends_request_stats():
            bench = Benchmark(MagicMock())
            bench.progress = MagicMock()

            bench._on_response('resp', 404, 10)

            assert_that(bench.stats[0].content_size, is_(4))
            assert_that(bench.stats[0].status_code, is_(404))
            assert_that(bench.stats[0].duration, is_(90))

    def describe_run():
        def it_stops_the_progress():
            bench = Benchmark(MagicMock())
            bench.progress = MagicMock()
            bench.requests = MagicMock()

            bench.run()

            assert_that(bench.progress.call_count, is_(0))
