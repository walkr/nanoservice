import time
from multiprocessing import Process
from nanoservice import Subscriber, Publisher

import util


def start_service(addr, n):
    """ Start a service """

    s = Subscriber(addr)

    def do_something(line):
        pass

    s.subscribe('test', do_something)

    started = time.time()
    for _ in range(n):
        s.process()
    s.sock.close()
    duration = time.time() - started

    print('Subscriber service stats:')
    util.print_stats(n, duration)
    return


def bench(client, n):
    """ Benchmark n requests """
    items = list(range(n))

    # Time client publish operations
    # ------------------------------
    started = time.time()
    for i in items:
        client.publish('test', i)
    duration = time.time() - started

    print('Publisher client stats:')
    util.print_stats(n, duration)


def run(N, addr):

    # Fork service
    service_process = Process(target=start_service, args=(addr, N))
    service_process.start()

    time.sleep(0.5)  # Wait for service connect
    # Create client and make reqs
    c = Publisher(addr)
    bench(c, N)
    c.sock.close()

    time.sleep(1)
    service_process.terminate()


if __name__ == '__main__':

    N = 100000

    print('')
    print('Pub-Sub over IPC')
    print('-----------------------------')
    run(N, 'ipc:///tmp/bench-pub-sub-ipc.sock')

    print('')
    print('Pub-Sub over TCP')
    print('-----------------------------')
    run(N, 'tcp://127.0.0.1:5053')
