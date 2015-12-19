'''
The MIT License (MIT)

Copyright (c) 2016 Tony Walker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import hmac
import hashlib

from .error import AuthenticatorInvalidSignature


class Authenticator(object):
    """ This object is used to authenticate messages """

    def __init__(self, secret, digestmod=None):
        assert secret
        self.secret = secret.encode('utf-8')
        self.digestmod = digestmod or hashlib.sha256
        self.sig_size = self.digestmod().digest_size * 2
        self._hmac = hmac.new(self.secret, digestmod=self.digestmod)

    def sign(self, encoded):
        """ Return authentication signature of encoded bytes """
        signature = self._hmac.copy()
        signature.update(encoded)
        return signature.hexdigest().encode('utf-8')

    def signed(self, encoded):
        """ Sign encoded bytes and append signature """
        signature = self.sign(encoded)
        return encoded + signature

    def unsigned(self, encoded):
        """ Remove signature and return just the message """
        message, _ = self.split(encoded)
        return message

    def split(self, encoded):
        """ Split into signature and message """
        maxlen = len(encoded) - self.sig_size
        message = encoded[:maxlen]
        signature = encoded[-self.sig_size:]
        return message, signature

    def auth(self, encoded):
        """ Validate integrity of encoded bytes """
        message, signature = self.split(encoded)
        computed = self.sign(message)
        if not hmac.compare_digest(signature, computed):
            raise AuthenticatorInvalidSignature
