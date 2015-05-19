import unittest

from nanoservice import crypto
from nanoservice import error


class TestAuthenticator(unittest.TestCase):

    def setUp(self):
        self.authenticator = crypto.Authenticator('my secret')

    def tearDown(self):
        pass

    def test_good_signature(self):
        message = b'message'
        signed_message = self.authenticator.signed(message)
        self.authenticator.auth(signed_message)

    def test_bad_signature(self):
        message = b'message'
        signed = self.authenticator.signed(message)
        print('signed msg is: ', signed)
        signed += b'123456789abacdef'
        print(signed)
        with self.assertRaises(error.AuthenticatorInvalidSignature):
            self.authenticator.auth(signed)

    def test_unsigned(self):
        message = b'my super secret message'
        signed = self.authenticator.signed(message)
        unsigned = self.authenticator.unsigned(signed)
        self.assertEqual(message, unsigned)

if __name__ == '__main__':
    unittest.main()
