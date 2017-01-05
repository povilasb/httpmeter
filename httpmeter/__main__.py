import sys

from . import net, cli, summary


def main(args) -> None:
    conf = cli.parse_args(args)
    requests = net.HttpRequests()\
        .verbose(False)\
        .show_progress(summary.Progress())
    requests.exec_to(conf.url, conf.concurrency, conf.requests)


if __name__ == '__main__':
    main(sys.argv[1:])
