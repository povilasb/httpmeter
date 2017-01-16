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

    def describe_completed_requests():
        def it_returns_request_stats_count():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(0, 200, 0),
                stats.ForRequest(0, 404, 0),
                stats.ForRequest(0, 200, 0),
            ])

            assert_that(bench_stats.completed_requests(), is_(3))

    def describe_summary():
        def it_returns_benchmark_results_with_minimum_content_size():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(40000, 200, 0),
                stats.ForRequest(6000, 404, 0),
                stats.ForRequest(65000, 200, 0),
            ])

            results = bench_stats.summary()

            assert_that(results.min_doc_len, is_(6000))

        def it_returns_benchmark_results_with_average_content_size():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(10000, 200, 0),
                stats.ForRequest(4000, 404, 0),
                stats.ForRequest(10000, 200, 0),
            ])

            results = bench_stats.summary()

            assert_that(results.avg_doc_len, is_(8000))

        def it_returns_benchmark_results_with_maximum_content_size():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(40000, 200, 0),
                stats.ForRequest(6000, 404, 0),
                stats.ForRequest(65000, 200, 0),
            ])

            results = bench_stats.summary()

            assert_that(results.max_doc_len, is_(65000))

        def it_returns_benchmark_results_with_concurrency():
            bench_stats = stats.ForBenchmark(
                [stats.ForRequest(40000, 200, 0)], 100)

            results = bench_stats.summary()

            assert_that(results.concurrency, is_(100))

        def it_returns_benchmark_results_with_completed_requests_count():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(40000, 200, 0),
                stats.ForRequest(6000, 404, 0),
                stats.ForRequest(65000, 200, 0),
            ])

            results = bench_stats.summary()

            assert_that(results.completed_requests, is_(3))

        def it_returns_benchmark_results_with_http_client_speed():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(40000, 200, 0),
                stats.ForRequest(6000, 404, 0),
                stats.ForRequest(65000, 200, 0),
            ], 1, 0.5)

            results = bench_stats.summary()

            assert_that(results.reqs_per_sec, is_(6))

        def it_returns_benchmark_results_with_min_avg_and_max_request_durations():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(40000, 200, 1.25),
                stats.ForRequest(6000, 404, 0.25),
                stats.ForRequest(65000, 200, 3),
            ])

            results = bench_stats.summary()

            assert_that(results.min_conn_time, is_(0.25))
            assert_that(results.avg_conn_time, is_(1.5))
            assert_that(results.max_conn_time, is_(3))

        def it_returns_benchmark_results_status_codes_stats():
            bench_stats = stats.ForBenchmark([
                stats.ForRequest(40000, 200, 0),
                stats.ForRequest(6000, 404, 0),
                stats.ForRequest(65000, 200, 0),
            ])

            results = bench_stats.summary()

            assert_that(results.status_codes, is_({404: 1, 200: 2}))
