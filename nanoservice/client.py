'''
The MIT License (MIT)

Copyright (c) 2014 Tony Walker

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

import uuid
import nanomsg
import logging

from .crypto import Authenticator
from .encoder import MsgPackEncoder


class Client(object):
    """ A requester client """

    def __init__(self, addr, encoder=None, socket=None,
                 auth=False, secret=None, digestmod=None):
        self.addr = addr
        self.encoder = encoder or MsgPackEncoder()
        self.sock = socket if socket else nanomsg.Socket(nanomsg.REQ)
        self.sock.connect(self.addr)
        self.authenticator = Authenticator(secret, digestmod) if auth else None

    def build_payload(self, method, args):
        ref = str(uuid.uuid4())
        return (method, args, ref)

    def encode(self, payload):
        return self.encoder.encode(payload)

    def decode(self, msg):
        return self.encoder.decode(msg)

    def send(self, payload):
        """ Send payload through the socket """
        payload = self.encode(payload)
        if self.authenticator:
            payload = self.authenticator.signed(payload)
        self.sock.send(payload)

    def receive(self):
        """ Receive response from socket """
        response = self.sock.recv()
        if self.authenticator:
            self.authenticator.auth(response)
            response = self.authenticator.unsigned(response)
        decoded = self.encoder.decode(response)
        return decoded

    def call(self, method, *args):
        """ Call the remote service """
        payload = self.build_payload(method, args)
        logging.debug('* Client will send payload: {}'.format(payload))
        self.send(payload)

        res = self.receive()
        assert payload[2] == res['ref']
        return res['result'], res['error']
