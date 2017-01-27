import argparse
from typing import List, Tuple


def parse_header(header: str) -> Tuple[str, str]:
    parts = header.split(':')
    return (parts[0].strip(), parts[1].strip())


class AppendHeader(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        name, value = parse_header(values)
        headers = getattr(namespace, self.dest)
        headers[name] = value


def parse_args(args: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--concurrency', metavar='N', default=1, type=int,
        help='Number of multiple requests to perform at a time'
    )
    parser.add_argument(
        '-H', '--header', metavar='custom-header', default={},
        type=str, action=AppendHeader, dest='headers',
        help='Append extra headers to the request.'
    )
    parser.add_argument(
        '-n', '--requests', metavar='N', default=1, type=int,
        help='Number of requests to perform for the benchmarking session.'
    )
    parser.add_argument(
        '-X', '--proxy', metavar='proxy:port', type=str,
        help='Use a proxy server for the requests.'
    )
    parser.add_argument(
        '--uvloop', dest='use_uvloop', default=False, action='store_true',
        help='Use uvloop to increase networking performance.',
    )
    parser.add_argument('url', metavar='URL', type=str)
    return parser.parse_args(args=args)
