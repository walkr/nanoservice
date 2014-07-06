import unittest
import logging
from multiprocessing import Process

from nanoservice import Service
from nanoservice import Client
from nanoservice import encoder


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.addr = 'ipc:///tmp/test-service01.sock'

    def tearDown(self):
        self.client.sock.close()

    def start_service(self, addr, encoder):
        s = Service(addr, encoder=encoder)
        s.register('divide', lambda x,y: x/y)
        s.start()


class TestEncodingDecoding(BaseTestCase):
    """ Test the communication between endpoints using various
    various mechanisms """

    def _run_test_with_encoder(self, encoder):
        proc = Process(
            target=self.start_service,
            args=(self.addr, encoder)
        )
        proc.start()
        self.client = Client(self.addr, encoder=encoder)
        res, err = self.client.call('divide', 10, 2)
        proc.terminate()
        expected = 5
        self.assertEqual(expected, res)

    def test_json_encoder(self):
        self._run_test_with_encoder(encoder.JSONEncoder())

    def test_msgpack_encoder(self):
        self._run_test_with_encoder(encoder.MsgPackEncoder())




if __name__ == '__main__':
    unittest.main()
