import time
from multiprocessing import Process
from nanoservice import Service, Client

import util


def start_service(addr, n, auth=False, secret=None):
    """ Start a service """
    s = Service(addr, auth=auth, secret=secret)
    s.register('add', lambda x, y: x+y)

    started = time.time()
    for _ in range(n):
        s.process()
    duration = time.time() - started

    time.sleep(0.1)
    print('Service stats:')
    util.print_stats(n, duration)
    return


def bench(client, n):
    """ Benchmark n requests """
    pairs = [(x, x+1) for x in range(n)]

    started = time.time()
    for pair in pairs:
        res, err = client.call('add', *pair)
        # assert err is None
    duration = time.time() - started
    print('Client stats:')
    util.print_stats(n, duration)


def run(N, addr):
    # Fork service
    service_process = Process(
        target=start_service, args=(addr, N, True, 'secret'))
    service_process.start()
    time.sleep(0.1)  # Wait for service to connect

    # Create client and make reqs
    c = Client(addr, auth=True, secret='secret')
    bench(c, N)
    c.sock.close()

    time.sleep(0.2)
    service_process.terminate()


if __name__ == '__main__':
    N = 20000

    print('')
    print('Req-Rep over IPC (w/ authentication)')
    print('-----------------------------')
    run(N, 'ipc:///tmp/bench-req-rep-ipc.sock')

    print('')
    print('Req-Rep over TCP (w/ authentication)')
    print('-----------------------------')
    run(N, 'tcp://127.0.0.1:5051')
