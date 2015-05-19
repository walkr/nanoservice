from multiprocessing import Process

from nanoservice import Service
from nanoservice import Client
from nanoservice import encoder


def check(res, expected):
    assert res == expected


def start_service(addr, encoder, auth=False, secret=None):
    """ Start a service with options """
    s = Service(addr, encoder=encoder, auth=auth, secret=secret)
    s.register('none', lambda: None)
    s.register('divide', lambda x, y: x/y)
    s.register('upper', lambda dct: {k: v.upper() for k, v in dct.items()})
    s.start()


# ------------------


TESTS = [
    (('divide', [10, 2]), 5.0),
    (('none', []), None),
    (('upper', [{'a': 'a'}]), {'a': 'A'})
]


def test_encoding():
    """ Test encoding with defferent options """
    addr = 'ipc:///tmp/test-service01.sock'

    auth_schemes = [(False, None), (True, 'my secret')]
    encoders = [encoder.JSONEncoder(), encoder.MsgPackEncoder()]

    for test, expected in TESTS:
        for enc in encoders:
            for scheme in auth_schemes:

                method, args = test
                auth, secret = scheme

                proc = Process(
                    target=start_service,
                    args=(addr, enc, auth, secret))
                proc.start()

                client = Client(addr, encoder=enc, auth=auth, secret=secret)
                res, err = client.call(method, *args)
                client.sock.close()
                proc.terminate()
                yield check, res, expected
                # self.assertEqual(expected, res)
