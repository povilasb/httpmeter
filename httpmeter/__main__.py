import sys

from . import net, cli


def main(args) -> None:
    conf = cli.parse_args(args)
    requests = net.HttpRequests()\
        .verbose(False)
    stats = requests.exec_to(conf.url, conf.concurrency, conf.requests)
    print(stats)


if __name__ == '__main__':
    main(sys.argv[1:])
