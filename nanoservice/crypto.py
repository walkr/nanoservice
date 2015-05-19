import hmac
import hashlib

from .error import AuthenticatorInvalidSignature


class Authenticator(object):
    """ This object is used to authenticate messages """

    def __init__(self, secret, digestmod=None, sep=b'::'):
        assert secret
        self.secret = secret.encode('utf-8')
        self.digestmod = digestmod or hashlib.sha256
        self.digest_size = self.digestmod().digest_size
        self.sep = sep

    def sign(self, encoded):
        """ Return authentication signature of encoded bytes """
        h = hmac.new(self.secret, encoded, digestmod=self.digestmod)
        return h.hexdigest().encode('utf-8')

    def signed(self, encoded):
        """ Sign encoded bytes and append signature """
        signature = self.sign(encoded)
        return encoded + self.sep + signature

    def unsigned(self, encoded):
        """ Remove signature and return just the message """
        message, _ = encoded.split(self.sep)
        return message

    def auth(self, encoded):
        """ Validate integrity of encoded bytes """
        message, signature = encoded.split(b'::')
        computed = self.sign(message)
        if not hmac.compare_digest(signature, computed):
            raise AuthenticatorInvalidSignature
