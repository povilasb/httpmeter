from hamcrest import assert_that, is_

from httpmeter import cli


def describe_parse_args():
    def it_returns_parsed_arguments():
        args = cli.parse_args(['-c', '100', 'http://example.com'])

        assert_that(args.concurrency, is_(100))
        assert_that(args.url, is_('http://example.com'))
