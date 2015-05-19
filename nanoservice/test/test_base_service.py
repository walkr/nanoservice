import unittest

from nanoservice import Service
from nanoservice import Client


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        addr = 'inproc://test'
        self.client = Client(addr)
        self.service = Service(addr)
        self.service.register('divide', lambda x,y: x/y)
        self.service.register('echo', lambda x: x)

    def tearDown(self):
        self.client.sock.close()
        self.service.sock.close()


class TestService(BaseTestCase):

    def test_register_method(self):
        f = lambda x: x
        self.service.register(f, 'afun')

    def test_recv_method(self):
        sent = ['a', 'b', 'c']
        encoded = self.client.encoder.encode(sent)
        self.client.sock.send(encoded)
        got = self.service.receive()
        self.assertEqual(sent, got)

    def test_send_method(self):
        sent = ['a', 'b', 'c']
        self.test_recv_method() # To send data to service
        self.service.send(sent)
        got = self.client.encoder.decode(self.client.sock.recv())
        self.assertEqual(sent, got)

    def test_execute_method_w_success(self):
        res = self.service.execute('divide', (6,2), None)
        expected = {'result': 3, 'error': None, 'ref': None}
        self.assertEqual(res, expected)

    def test_execute_method_w_error(self):
        res = self.service.execute('divide', (1,0), None)
        self.assertIsNotNone(res['error'])

    def test_encoder(self):
        data = {'name': 'Joe Doe'}
        encoded = self.service.encoder.encode(data)
        decoded = self.service.encoder.decode(encoded)
        self.assertEqual(data, decoded)


if __name__ == '__main__':
    unittest.main()
