from . import net


def main() -> None:
    requests = net.HttpRequests().verbose(True)
    stats = requests.exec_to('https://httpbin.org/ip', 1, 1)
    print(stats)


if __name__ == '__main__':
    main()
