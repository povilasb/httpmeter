import argparse
from typing import List


def parse_args(args: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--concurrency', metavar='N', default=1, type=int,
        help='Number of multiple requests to perform at a time'
    )
    parser.add_argument(
        '-H', '--header', metavar='custom-header', default=[],
        nargs='*', type=str,
        help='Append extra headers to the request.'
    )
    parser.add_argument(
        '-n', '--requests', metavar='N', default=1, type=int,
        help='Number of requests to perform for the benchmarking session'
    )
    parser.add_argument(
        '-P', '--proxy-auth',
        metavar='proxy-auth-username:password', type=str,
        help='Supply BASIC Authentication credentials to a proxy en-route.'
    )
    parser.add_argument(
        '-X', '--proxy', metavar='proxy:port', type=str,
        help='Use a proxy server for the requests.'
    )
    parser.add_argument('url', metavar='URL', type=str)
    return parser.parse_args(args=args)
