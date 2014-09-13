import time
from multiprocessing import Process
from nanoservice import Service, Client

import util


def start_service(addr, n):
    """ Start a service """
    s = Service(addr)

    started = time.time()
    for _ in range(n):
        msg = s.sock.recv()
        s.sock.send(msg)
    s.sock.close()
    duration = time.time() - started

    print('Raw REP service stats:')
    util.print_stats(n, duration)
    return


def bench(client, n):
    """ Benchmark n requests """
    items = list(range(n))

    # Time client publish operations
    # ------------------------------
    started = time.time()
    msg = b'x'
    for i in items:
        client.sock.send(msg)
        res = client.sock.recv()
        assert msg == res
    duration = time.time() - started

    print('Raw REQ client stats:')
    util.print_stats(n, duration)


def run(N, addr):

    # Fork service
    service_process = Process(target=start_service, args=(addr, N))
    service_process.start()

    time.sleep(0.1)  # Wait for service connect
    # Create client and make reqs
    c = Client(addr)
    bench(c, N)
    c.sock.close()

    time.sleep(0.2)
    service_process.terminate()


if __name__ == '__main__':

    N = 50000

    print('')
    print('Req-Rep over IPC (raw)')
    print('-----------------------------')
    run(N, 'ipc:///tmp/bench-raw-reqrep-ipc.sock')

    print('')
    print('Req-Rep over TCP (raw)')
    print('-----------------------------')
    run(N, 'tcp://127.0.0.1:5052')
