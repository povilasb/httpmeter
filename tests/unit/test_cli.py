from hamcrest import assert_that, is_

from httpmeter import cli


def describe_parse_args():
    def it_returns_parsed_arguments():
        args = cli.parse_args(['-c', '100', 'http://example.com'])

        assert_that(args.concurrency, is_(100))
        assert_that(args.url, is_('http://example.com'))

    def describe_when_multiple_headers_are_provided():
        def it_returns_them_all():
            args = cli.parse_args([
                '-H', 'Connection: close',
                '-H', 'User-Agent: curl',
                '-c', '1',
                'http://example.com'
            ])

            assert_that(args.headers, is_({'Connection': 'close',
                                           'User-Agent': 'curl'}))


def describe_parse_header():
    def it_returns_header_name_and_value_as_a_tuple():
        header, value = cli.parse_header('Connection: close')

        assert_that(header, is_('Connection'))
        assert_that(value, is_('close'))

    def describe_when_header_value_has_trailing_whitespaces():
        def it_removes_them():
            _, value = cli.parse_header('Connection:   close   ')

            assert_that(value, is_('close'))
