import unittest
import logging
from multiprocessing import Process

from nanoservice import SubService
from nanoservice import PubClient


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.addr = 'inproc://test'
        self.client = PubClient(self.addr)
        self.service = SubService(self.addr)
        self.service.subscribe('upper', lambda line: line.upper())
        self.service.subscribe('lower', lambda line: line.lower())

    def tearDown(self):
        self.client.sock.close()
        self.service.sock.close()


class TestPubSub(BaseTestCase):

    def test_pub_sub(self):
        # Client side
        line = 'hello world'
        self.client.publish('upper', line)
        self.client.publish('lower', line.upper())

        # Server side
        uppercase = self.service.process()
        self.assertEqual(uppercase, line.upper())

        lowercase = self.service.process()
        self.assertEqual(lowercase, line.lower())


if __name__ == '__main__':
    unittest.main()
