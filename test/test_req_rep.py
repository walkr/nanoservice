import unittest
import logging
from multiprocessing import Process

from nanoservice import Service
from nanoservice import Client


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.addr = 'ipc:///tmp/test-service01.sock'

    def tearDown(self):
        self.client.sock.close()

    def start_service(self, addr):
        s = Service(addr)
        s.register('divide', lambda x,y: x/y)
        s.start()

class TestTCPProtocol(BaseTestCase):

    def make_req(self, *args):
        proc = Process(target=self.start_service, args=(self.addr,))
        proc.start()
        self.client = Client(self.addr)
        res, err = self.client.call('divide', *args)
        proc.terminate()
        return res, err

    def test_req_rep_w_success(self):
        res, err = self.make_req(6,2)
        self.assertEqual(3, res)
        self.assertTrue(err is None)

    def test_req_rep_w_error(self):
        res, err = self.make_req(6,0)
        self.assertTrue(res is None)
        self.assertTrue(err is not None)


if __name__ == '__main__':
    unittest.main()
