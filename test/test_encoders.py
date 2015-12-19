import hashlib
from multiprocessing import Process

from nanoservice import Responder
from nanoservice import Requester
from nanoservice import encoder
from nanoservice import Authenticator


def check(res, expected):
    assert res == expected


def start_service(addr, encoder, authenticator=None):
    """ Start a service with options """
    s = Responder(addr, encoder=encoder, authenticator=authenticator)
    s.register('none', lambda: None)
    s.register('divide', lambda x, y: x / y)
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

    authenticators = [None, Authenticator('my-secret', hashlib.sha256)]
    encoders = [encoder.JSONEncoder(), encoder.MsgPackEncoder()]

    for test, expected in TESTS:
        for enc in encoders:
            for authenticator in authenticators:

                method, args = test
                proc = Process(
                    target=start_service,
                    args=(addr, enc, authenticator))
                proc.start()

                client = Requester(addr, encoder=enc,
                                   authenticator=authenticator)
                res, err = client.call(method, *args)
                client.socket.close()
                proc.terminate()
                yield check, res, expected
                # self.assertEqual(expected, res)
