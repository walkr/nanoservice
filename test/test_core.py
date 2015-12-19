import unittest

from nanoservice import Subscriber
from nanoservice import Publisher


class EndpointTest(unittest.TestCase):

    def setUp(self):
        self.addr = 'inproc://test'
        self.client = Publisher(self.addr)
        self.service = Subscriber(self.addr)
        self.service.subscribe('upper', lambda line: line.upper())
        self.service.subscribe('lower', lambda line: line.lower())

    def tearDown(self):
        self.client.socket.close()
        self.service.socket.close()


class CommunicatorTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
