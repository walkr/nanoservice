import time
import nanomsg
from multiprocessing import Process
from nanoservice import SubService, PubClient

import util


def start_service(addr, n):
    """ Start a service """

    s = SubService(addr)
    s.sock.set_string_option(nanomsg.SUB, nanomsg.SUB_SUBSCRIBE, 'test')

    started = time.time()
    for _ in range(n):
        msg = s.sock.recv()
    s.sock.close()
    duration = time.time() - started

    print('Raw SUB service stats:\n')
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
        client.sock.send(msg)
    duration = time.time() - started

    print('Raw PUB client stats:\n')
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
    print('------------------------------')
    print('Benchmark raw PUB-SUB over IPC')
    print('------------------------------\n')
    run(N, 'ipc:///tmp/bench-pub-sub-ipc.sock')

    print('------------------------------')
    print('Benchmark raw PUB-SUB over TCP')
    print('------------------------------\n')
    run(N, 'tcp://127.0.0.1:5050')
