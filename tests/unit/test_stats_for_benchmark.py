from hamcrest import assert_that, is_

from httpmeter import stats


def describe_ForBenchmark():
    def describe_content_sizes():
        def it_returns_iterable_of_content_sizes_for_all_requests():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(100, 0, 0),
                stats.ForRequest(200, 0, 0),
                stats.ForRequest(300, 0, 0),
            ])

            sizes = list(bench_stats.content_sizes())

            assert_that(sizes, is_([100, 200, 300]))

    def describe_durations():
        def it_returns_iterable_of_durations_for_all_requests():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(0, 0, 0.1),
                stats.ForRequest(0, 0, 0.2),
                stats.ForRequest(0, 0, 0.3),
            ])

            durations = list(bench_stats.durations())

            assert_that(durations, is_([0.1, 0.2, 0.3]))

    def describe_status_codes():
        def it_returns_status_codes_count_dictionary():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(0, 200, 0),
                stats.ForRequest(0, 404, 0),
                stats.ForRequest(0, 200, 0),
            ])

            status_codes = bench_stats.status_codes()

            assert_that(status_codes, is_({200: 2, 404: 1}))

    def describe_completed_results():
        def it_returns_request_stats_count():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(0, 200, 0),
                stats.ForRequest(0, 404, 0),
                stats.ForRequest(0, 200, 0),
            ])

            assert_that(bench_stats.completed_results(), is_(3))
