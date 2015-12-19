import unittest

from nanoservice import Responder
from nanoservice import Requester

from nanoservice import error
from nanoservice import crypto


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        addr = 'inproc://test'
        self.client = Requester(addr)
        self.service = Responder(addr)
        self.service.register('divide', lambda x, y: x / y)
        self.service.register('echo', lambda x: x)

    def tearDown(self):
        self.client.socket.close()
        self.service.socket.close()


class TestResponder(BaseTestCase):

    def test_register_method(self):
        f = lambda x: x
        self.service.register(f, 'afun')

    def test_recv_method(self):
        sent = ['a', 'b', 'c']
        encoded = self.client.encoder.encode(sent)
        self.client.socket.send(encoded)
        got = self.service.receive()
        self.assertEqual(sent, got)

    def test_send_method(self):
        sent = ['a', 'b', 'c']
        self.test_recv_method()  # To send data to service
        self.service.send(sent)
        got = self.client.encoder.decode(self.client.socket.recv())
        self.assertEqual(sent, got)

    def test_execute_method_w_success(self):
        res = self.service.execute('divide', (6, 2), None)
        expected = {'result': 3, 'error': None, 'ref': None}
        self.assertEqual(res, expected)

    def test_execute_method_w_error(self):
        res = self.service.execute('divide', (1, 0), None)
        self.assertIsNotNone(res['error'])

    def test_encoder(self):
        data = {'name': 'Joe Doe'}
        encoded = self.service.encoder.encode(data)
        decoded = self.service.encoder.decode(encoded)
        self.assertEqual(data, decoded)

    def test_service_authenticate_simple(self):
        payload = 'no authentication set up. payload will be unchanged'
        got = self.service.verify(payload)
        self.assertEqual(got, payload)

    # Test error throwing

    def test_payload_decode_error(self):
        self.client.socket.send('"abc')
        self.assertRaises(error.DecodeError, self.service.receive)

    def test_payload_parse_error(self):
        for payload in [[1, 2], '', None]:
            self.assertRaises(
                error.RequestParseError, self.service.parse, payload)

    def test_payload_authenticate_error(self):
        payload = 'abc'
        auth = crypto.Authenticator('my secret')
        auth.unsigned = None  # Overwrite method to force error

        self.service.authenticator = auth
        self.client.authenticator = auth

        payload = self.client.encode(payload)
        payload = auth.signed(payload)
        self.client.socket.send(payload)
        self.assertRaises(
            error.AuthenticateError, self.service.receive)

    def test_payload_authenticator_invalid_signature(self):
        payload = 'abc'
        auth = crypto.Authenticator('my secret')
        self.service.authenticator = auth
        self.client.authenticator = auth

        payload = self.client.encode(payload)
        payload = auth.signed(payload)
        self.client.socket.send(b'123' + payload)
        self.assertRaises(
            error.AuthenticatorInvalidSignature, self.service.receive)


if __name__ == '__main__':
    unittest.main()
