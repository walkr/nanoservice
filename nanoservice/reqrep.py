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

import uuid
import nanomsg
import logging

from .error import DecodeError
from .error import RequestParseError
from .error import AuthenticateError
from .error import AuthenticatorInvalidSignature
from .encoder import MsgPackEncoder

from .core import Endpoint
from .core import Process


class Responder(Endpoint, Process):
    """ A service which responds to requests """

    # pylint: disable=too-many-arguments
    # pylint: disable=no-member
    def __init__(self, address, encoder=None, authenticator=None,
                 socket=None, bind=True, timeouts=(None, None)):

        # Defaults
        socket = socket or nanomsg.Socket(nanomsg.REP)
        encoder = encoder or MsgPackEncoder()

        super(Responder, self).__init__(
            socket, address, bind, encoder, authenticator, timeouts)

        self.methods = {}
        self.descriptions = {}

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
            logging.error(
                'Service error while authenticating request: {}'
                .format(exception), exc_info=1)

        except AuthenticatorInvalidSignature as exception:
            logging.error(
                'Service error while authenticating request: {}'
                .format(exception), exc_info=1)

        except DecodeError as exception:
            logging.error(
                'Service error while decoding request: {}'
                .format(exception), exc_info=1)

        except RequestParseError as exception:
            logging.error(
                'Service error while parsing request: {}'
                .format(exception), exc_info=1)

        else:
            logging.debug('Service received payload: {}'.format(payload))

        if response:
            self.send(response)
        else:
            self.send('')


class Requester(Endpoint):
    """ A requester client """

    # pylint: disable=too-many-arguments
    # pylint: disable=no-member
    def __init__(self, address, encoder=None, authenticator=None,
                 socket=None, bind=False, timeouts=(None, None)):

        # Defaults
        socket = socket or nanomsg.Socket(nanomsg.REQ)
        encoder = encoder or MsgPackEncoder()

        super(Requester, self).__init__(
            socket, address, bind, encoder, authenticator, timeouts)

    @classmethod
    def build_payload(cls, method, args):
        """ Build the payload to be sent to a `Responder` """
        ref = str(uuid.uuid4())
        return (method, args, ref)

    # pylint: disable=logging-format-interpolation
    def call(self, method, *args):
        """ Make a call to a `Responder` and return the result """

        payload = self.build_payload(method, args)
        logging.debug('* Client will send payload: {}'.format(payload))
        self.send(payload)

        res = self.receive()
        assert payload[2] == res['ref']
        return res['result'], res['error']
