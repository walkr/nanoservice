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

from .encoder import MsgPackEncoder
from .error import ClientError


class Client(object):
    """ A requester client """

    def __init__(self, addr, encoder=None, socket=None):
        self.addr = addr
        self.encoder = encoder or MsgPackEncoder()
        self.sock = socket if socket else nanomsg.Socket(nanomsg.REQ)
        self.sock.connect(self.addr)

    def build_payload(self, method, args):
        ref = str(uuid.uuid4())
        return (method, args, ref)

    def encode(self, payload):
        return self.encoder.encode(payload)

    def decode(self, msg):
        return self.encoder.decode(msg)

    def call(self, method, *args):
        payload = self.build_payload(method, args)
        self.sock.send(self.encode(payload))
        res = self.decode(self.sock.recv())
        assert payload[2] == res['ref']
        return res['result'], res['error']


class PubClient(Client):
    """ A publisher client """

    def __init__(self, addr, encoder=None):
        socket = nanomsg.Socket(nanomsg.PUB)
        super(PubClient, self).__init__(addr, encoder, socket)

    def call(self, method, *args):
        raise ClientError('Operation not allowed on this type of client')

    def build_payload(self, tag, data):
        payload = bytes(tag.encode('utf-8')) + self.encode(data)
        return payload

    def publish(self, tag, data):
        payload = self.build_payload(tag, data)
        self.sock.send(payload)
