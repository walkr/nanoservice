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

import sys
import signal
import logging
import threading
import nanomsg

from .error import EncodeError
from .error import DecodeError
from .error import AuthenticateError
from .error import AuthenticatorInvalidSignature
from .error import EndpointError


class Endpoint(object):

    """ An Endpoints sends and receives messages

    Processing incoming messages:
        socket receive -> verify(*) -> decode

    Processing outgoing messages:
        encode -> sign(*) -> socket send

    (*) Sign/Verify only if authenticator is available
    """

    # pylint: disable=too-many-arguments
    # pylint: disable=no-member
    def __init__(self, socket, address, bind, encoder, authenticator,
                 timeouts=(None, None)):

        # timeouts must be a pair of the form:
        # (send-timeout-value, recv-timeout-value)

        self.socket = socket
        self.address = address
        self.bind = bind
        self.encoder = encoder
        self.authenticator = authenticator
        self.initialize(timeouts)

    def initialize(self, timeouts):
        """ Bind or connect the nanomsg socket to some address """

        # Bind or connect to address
        if self.bind is True:
            self.socket.bind(self.address)
        else:
            self.socket.connect(self.address)

        # Set send and recv timeouts
        self._set_timeouts(timeouts)

    def _set_timeouts(self, timeouts):
        """ Set socket timeouts for send and receive respectively """

        (send_timeout, recv_timeout) = (None, None)

        try:
            (send_timeout, recv_timeout) = timeouts
        except TypeError:
            raise EndpointError(
                '`timeouts` must be a pair of numbers (2, 3) which represent '
                'the timeout values for send and receive respectively')

        if send_timeout is not None:
            self.socket.set_int_option(
                nanomsg.SOL_SOCKET, nanomsg.SNDTIMEO, send_timeout)

        if recv_timeout is not None:
            self.socket.set_int_option(
                nanomsg.SOL_SOCKET, nanomsg.RCVTIMEO, recv_timeout)

    def send(self, payload):
        """ Encode and sign (optional) the send through socket """
        payload = self.encode(payload)
        payload = self.sign(payload)
        self.socket.send(payload)

    def receive(self, decode=True):
        """ Receive from socket, authenticate and decode payload """
        payload = self.socket.recv()
        payload = self.verify(payload)
        if decode:
            payload = self.decode(payload)
        return payload

    def sign(self, payload):
        """ Sign payload using the supplied authenticator """
        if self.authenticator:
            return self.authenticator.signed(payload)
        return payload

    def verify(self, payload):
        """ Verify payload authenticity via the supplied authenticator """
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

    def encode(self, payload):
        """ Encode payload """
        try:
            return self.encoder.encode(payload)
        except Exception as exception:
            raise EncodeError(str(exception))


class Process(object):
    """ A long running process """

    def start(self):
        """ Start and listen for calls """

        if threading.current_thread().name == 'MainThread':
            signal.signal(signal.SIGINT, self.stop)

        logging.info('Started on {}'.format(self.address))

        while True:
            self.process()

    def stop(self, dummy_signum=None, dummy_frame=None):
        """ Shutdown process (this method is also a signal handler) """
        logging.info('Shutting down ...')
        self.socket.close()
        sys.exit(0)
