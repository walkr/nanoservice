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
        fake_sig = self.authenticator.digestmod('fake'.encode('utf-8'))
        fake_sig = fake_sig.hexdigest().encode('utf-8')
        signed = fake_sig + signed[len(fake_sig):]
        with self.assertRaises(error.AuthenticatorInvalidSignature):
            self.authenticator.auth(signed)

    def test_unsigned(self):
        message = b'my super secret message'
        signed = self.authenticator.signed(message)
        print('signed is:', signed)
        unsigned = self.authenticator.unsigned(signed)
        self.assertEqual(message, unsigned)

if __name__ == '__main__':
    unittest.main()
