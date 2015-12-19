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

import nanomsg
import logging

from .error import SubscriberError
from .error import DecodeError
from .error import RequestParseError
from .error import AuthenticateError
from .error import AuthenticatorInvalidSignature
from .core import Endpoint
from .encoder import MsgPackEncoder


class Subscriber(Endpoint):
    """ A Subscriber executes various functions in response to
    different subscriptions it is subscribed to """

    # pylint: disable=too-many-arguments
    # pylint: disable=no-member
    def __init__(self, address, encoder=None, authenticator=None,
                 socket=None, bind=True, timeouts=(None, None)):

        # Defaults
        socket = socket or nanomsg.Socket(nanomsg.SUB)
        encoder = encoder or MsgPackEncoder()

        super(Subscriber, self).__init__(
            socket, address, bind, encoder, authenticator, timeouts)

        self.methods = {}
        self.descriptions = {}

    def parse(self, subscription):
        """ Fetch the function registered for a certain subscription """

        for name in self.methods:
            tag = bytes(name.encode('utf-8'))
            if subscription.startswith(tag):
                fun = self.methods.get(name)
                message = subscription[len(tag):]
                return tag, message, fun
        return None, None, None

    def register(self, name, fun, description=None):
        raise SubscriberError('Operation not allowed on this type of service')

    # pylint: disable=no-member
    def subscribe(self, tag, fun, description=None):
        """ Subscribe to something and register a function """
        self.methods[tag] = fun
        self.descriptions[tag] = description
        self.socket.set_string_option(nanomsg.SUB, nanomsg.SUB_SUBSCRIBE, tag)

    # pylint: disable=logging-format-interpolation
    # pylint: disable=duplicate-code
    def process(self):
        """ Receive a subscription from the socket and process it """

        subscription = None
        result = None

        try:
            subscription = self.socket.recv()

        except AuthenticateError as exception:
            logging.error(
                'Subscriber error while authenticating request: {}'
                .format(exception), exc_info=1)

        except AuthenticatorInvalidSignature as exception:
            logging.error(
                'Subscriber error while authenticating request: {}'
                .format(exception), exc_info=1)

        except DecodeError as exception:
            logging.error(
                'Subscriber error while decoding request: {}'
                .format(exception), exc_info=1)

        except RequestParseError as exception:
            logging.error(
                'Subscriber error while parsing request: {}'
                .format(exception), exc_info=1)

        else:
            logging.debug(
                'Subscriber received payload: {}'
                .format(subscription))

        _tag, message, fun = self.parse(subscription)
        message = self.verify(message)
        message = self.decode(message)

        try:
            result = fun(message)
        except Exception as exception:
            logging.error(exception, exc_info=1)

        # Return result to check successful execution of `fun` when testing
        return result


class Publisher(Endpoint):
    """ A Publisher sends messages down the nanomsg socket """

    # pylint: disable=too-many-arguments
    # pylint: disable=no-member
    def __init__(self, address, encoder=None, authenticator=None,
                 socket=None, bind=False, timeouts=(None, None)):

        # Defaults
        socket = socket or nanomsg.Socket(nanomsg.PUB)
        encoder = encoder or MsgPackEncoder()

        super(Publisher, self).__init__(
            socket, address, bind, encoder, authenticator, timeouts)

    def build_payload(self, tag, message):
        """ Encode, sign payload(optional) and attach subscription tag """
        message = self.encode(message)
        message = self.sign(message)
        payload = bytes(tag.encode('utf-8')) + message
        return payload

    def publish(self, tag, message):
        """ Publish a message down the socket """
        payload = self.build_payload(tag, message)
        self.socket.send(payload)
