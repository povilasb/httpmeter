from unittest.mock import MagicMock, patch

from hamcrest import assert_that, is_

from httpmeter.__main__ import Benchmark


def describe_Bencmark():
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
