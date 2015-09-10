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

import sys
import signal
import nanomsg
import logging
import threading

from .crypto import Authenticator
from .encoder import MsgPackEncoder

from .error import DecodeError
from .error import RequestParseError
from .error import AuthenticateError
from .error import AuthenticatorInvalidSignature


class Service(object):
    """ A Requester service"""

    # pylint: disable=too-many-arguments
    def __init__(self, addr, encoder=None, socket=None,
                 auth=False, secret=None, digestmod=None):
        self.addr = addr
        self.encoder = encoder or MsgPackEncoder()
        self.methods = {}
        self.descriptions = {}
        self.sock = socket if socket else nanomsg.Socket(nanomsg.REP)
        self.sock.bind(self.addr)
        self.authenticator = Authenticator(secret, digestmod) if auth else None

    def authenticate(self, payload):
        """ Authenticate payload then return unsigned payload """
        if not self.authenticator:
            return payload
        try:
            self.authenticator.auth(payload)
            return self.authenticator.unsigned(payload)
        except AuthenticatorInvalidSignature:
            raise
        except Exception as exception:
            raise AuthenticateError(str(exception))

    def decode(self, payload):
        """ Decode payload """
        try:
            return self.encoder.decode(payload)
        except Exception as exception:
            raise DecodeError(str(exception))

    def receive(self):
        """ Receive from socket, authenticate and decode payload """
        payload = self.sock.recv()
        payload = self.authenticate(payload)
        payload = self.decode(payload)
        return payload

    def send(self, response):
        """ Encode and sign (optional) the send through socket """
        response = self.encoder.encode(response)
        if self.authenticator:
            response = self.authenticator.signed(response)
        self.sock.send(response)

    def execute(self, method, args, ref):
        """ Execute the method with args """

        response = {'result': None, 'error': None, 'ref': ref}
        fun = self.methods.get(method)
        if not fun:
            response['error'] = 'Method `{}` not found'.format(method)
        else:
            try:
                response['result'] = fun(*args)
            except Exception as exception:
                logging.error(exception, exc_info=1)
                response['error'] = str(exception)
        return response

    def register(self, name, fun, description=None):
        """ Register function on this service """
        self.methods[name] = fun
        self.descriptions[name] = description

    @classmethod
    def parse(cls, payload):
        """ Parse client request """
        try:
            method, args, ref = payload
        except Exception as exception:
            raise RequestParseError(exception)
        else:
            return method, args, ref

    # pylint: disable=logging-format-interpolation
    def process(self):
        """ Receive data from socket and process request """

        response = None

        try:
            payload = self.receive()
            method, args, ref = self.parse(payload)
            response = self.execute(method, args, ref)

        except AuthenticateError as exception:
            logging.error('Service Error in authenticate {}'.format(exception), exc_info=1)

        except AuthenticatorInvalidSignature as exception:
            logging.error('Service Error authenticating {}'.format(exception), exc_info=1)

        except DecodeError as exception:
            logging.error('Service Error authenticating {}'.format(exception), exc_info=1)

        except RequestParseError as exception:
            logging.error('Service Error parsing {}'.format(exception), exc_info=1)

        else:
            logging.debug('Service Server received payload: {}'.format(payload))

        if response:
            self.send(response)
        else:
            self.send('')

    def start(self):
        """ Start and listen for calls """

        if threading.current_thread().name == 'MainThread':
            signal.signal(signal.SIGINT, self.stop)

        logging.info('* Service started on {}'.format(self.addr))
        while True:
            self.process()

    def stop(self):
        """Shut down the service"""
        logging.info('* Shutting down service ...')
        self.sock.close()
        sys.exit(0)
