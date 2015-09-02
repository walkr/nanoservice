import unittest

from nanoservice import Service
from nanoservice import Client


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        addr = 'inproc://test'
        self.client = Client(addr)
        self.service = Service(addr)
        self.service.register('divide', lambda x, y: x/y)
        self.service.register('echo', lambda x: x)

    def tearDown(self):
        self.client.sock.close()
        self.service.sock.close()


class TestClient(BaseTestCase):

    def test_build_payload(self):
        payload = self.client.build_payload('echo', 'My Name')
        method, args, ref = payload
        self.assertTrue(method == 'echo')
        self.assertTrue(len(payload) == 3)

    def test_encoder(self):
        data = {'name': 'Joe Doe'}
        encoded = self.client.encode(data)
        decoded = self.client.decode(encoded)
        self.assertEqual(data, decoded)

    def test_call_wo_receive(self):
        # Client side ops
        method, args = 'echo', 'hello world'
        payload = self.client.build_payload(method, args)
        self.client.sock.send(self.client.encode(payload))
        # Service side ops
        method, args, ref = self.service.receive()
        self.assertEqual(method, 'echo')
        self.assertEqual(args, 'hello world')
        self.assertEqual(ref, payload[2])

    def test_basic_socket_operation(self):
        msg = 'abc'
        self.client.sock.send(msg)
        res = self.service.sock.recv().decode('utf-8')
        self.assertEqual(msg, res)


if __name__ == '__main__':
    unittest.main()
