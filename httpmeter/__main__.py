from . import net


def main() -> None:
    requests = net.HttpRequests().verbose(True).via_proxy('http://localhost:8081')
    stats = requests.exec_to('https://httpbin.org/ip', 1, 3)
    print(stats)


if __name__ == '__main__':
    main()
