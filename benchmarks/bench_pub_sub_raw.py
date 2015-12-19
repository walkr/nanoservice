import time
import nanomsg
from multiprocessing import Process
from nanoservice import Subscriber, Publisher

import util


def start_service(addr, n):
    """ Start a service """

    s = Subscriber(addr)
    s.socket.set_string_option(nanomsg.SUB, nanomsg.SUB_SUBSCRIBE, 'test')

    started = time.time()
    for _ in range(n):
        msg = s.socket.recv()
    s.socket.close()
    duration = time.time() - started

    print('Raw SUB service stats:')
    util.print_stats(n, duration)
    return


def bench(client, n):
    """ Benchmark n requests """
    items = list(range(n))

    # Time client publish operations
    # ------------------------------
    started = time.time()
    msg = b'test line'
    for i in items:
        client.socket.send(msg)
    duration = time.time() - started

    print('Raw PUB client stats:')
    util.print_stats(n, duration)


def run(N, addr):

    # Fork service
    service_process = Process(target=start_service, args=(addr, N))
    service_process.start()

    time.sleep(0.5)  # Wait for service connect
    # Create client and make reqs
    c = Publisher(addr)
    bench(c, N)
    c.socket.close()

    time.sleep(1)
    service_process.terminate()


if __name__ == '__main__':

    N = 100000

    print('')
    print('Pub-Sub over IPC (raw)')
    print('-----------------------------')
    run(N, 'ipc:///tmp/bench-pub-sub-ipc.sock')

    print('')
    print('Pub-Sub over TCP (raw)')
    print('-----------------------------')
    run(N, 'tcp://127.0.0.1:5054')
