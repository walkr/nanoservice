import time
from multiprocessing import Process
from nanoservice import SubService, PubClient

import util


def start_service(addr, n):
    """ Start a service """

    s = SubService(addr)
    def do_something(line):
        pass
    s.subscribe('test', do_something)

    started = time.time()
    for _ in range(n):
        s.process()
    s.sock.close()
    duration = time.time() - started

    print('Subscriber service stats:\n')
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

    print('Publisher client stats:\n')
    util.print_stats(n, duration)

def run(N, addr):

    # Fork service
    service_process = Process(target=start_service, args=(addr,N))
    service_process.start()

    time.sleep(0.5) # Wait for service connect
    # Create client and make reqs
    c = PubClient(addr)
    bench(c, N)
    c.sock.close()

    time.sleep(1)
    service_process.terminate()


if __name__ == '__main__':

    N = 100000
    print('')
    print('-----------------------------')
    print('Benchmark PUB-SUB over IPC')
    print('-----------------------------\n')
    run(N, 'ipc:///tmp/bench-pub-sub-ipc.sock')

    print('-----------------------------')
    print('Benchmark PUB-SUB over TCP')
    print('-----------------------------\n')
    run(N, 'tcp://127.0.0.1:5050')
