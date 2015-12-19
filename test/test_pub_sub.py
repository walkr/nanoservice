import unittest

from nanoservice import Subscriber
from nanoservice import Publisher
from nanoservice import Authenticator


class BaseTestCase(unittest.TestCase):

    def setUp(self, authenticator=None):
        self.addr = 'inproc://test'
        self.client = Publisher(self.addr, authenticator=authenticator)
        self.service = Subscriber(self.addr, authenticator=authenticator)
        self.service.subscribe('upper', lambda line: line.upper())
        self.service.subscribe('lower', lambda line: line.lower())

    def tearDown(self):
        self.client.socket.close()
        self.service.socket.close()


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


class TestPubWithAuthentication(BaseTestCase):

    def setUp(self):
        authenticator = Authenticator('my-secret')
        super(TestPubWithAuthentication, self).setUp(authenticator)

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
