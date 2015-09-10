"""Nanoservice PUBSUB"""

import nanomsg
import logging

from .service import Service
from .client import Client

from .error import SubscriberError
from .error import PublisherError

from .error import DecodeError
from .error import RequestParseError
from .error import AuthenticateError
from .error import AuthenticatorInvalidSignature


class Subscriber(Service):
    """ Subscriber """

    #pylint: disable=too-many-arguments
    def __init__(self, addr, encoder=None,
                 auth=False, secret=None, digestmod=None):
        socket = nanomsg.Socket(nanomsg.SUB)
        super(Subscriber, self).__init__(
            addr, encoder, socket, auth, secret, digestmod)

    def get_fun_and_data(self, subscription):
        """ Fetch the function registered for a certain subscription """

        for name in self.methods:
            tag = bytes(name.encode('utf-8'))
            if subscription.startswith(tag):
                fun = self.methods.get(name)
                data = self.encoder.decode(subscription[len(tag):])
                return fun, data
        return None, None

    def register(self, name, fun, description=None):
        raise SubscriberError('Operation not allowed on this type of service')

    def subscribe(self, tag, fun):
        """ Subscribe and register a function """
        super(Subscriber, self).register(tag, fun)
        self.sock.set_string_option(nanomsg.SUB, nanomsg.SUB_SUBSCRIBE, tag)

    def receive(self):
        """ Receive request from client """
        payload = self.sock.recv()
        if self.authenticator:
            self.authenticator.auth(payload)
            payload = self.authenticator.unsigned(payload)
        return payload

    # pylint: disable=logging-format-interpolation
    # pylint: disable=duplicate-code
    def process(self):

        try:
            subscription = self.receive()

        except AuthenticateError as exception:
            logging.error('PubSub Error in authenticate {}'.format(exception), exc_info=1)

        except AuthenticatorInvalidSignature as exception:
            logging.error('PubSub Error authenticating {}'.format(exception), exc_info=1)

        except DecodeError as exception:
            logging.error('PubSub Error authenticating {}'.format(exception), exc_info=1)

        except RequestParseError as exception:
            logging.error('PubSub Error parsing {}'.format(exception), exc_info=1)

        else:
            logging.debug('PubSub Server received payload: {}'.format(subscription))

        fun, data = self.get_fun_and_data(subscription)

        result = None
        try:
            result = fun(data)
        except Exception as exception:
            logging.error(exception, exc_info=1)

        # Return result to check successful execution of `fun` when testing
        return result


class Publisher(Client):
    """ Publisher """

    #pylint: disable=too-many-arguments
    def __init__(self, addr, encoder=None,
                 auth=False, secret=None, digestmod=None):
        socket = nanomsg.Socket(nanomsg.PUB)
        super(Publisher, self).__init__(
            addr, encoder, socket, auth, secret, digestmod)

    def call(self, method, *args):
        raise PublisherError('Operation not allowed')

    def send(self, payload):
        """ Send payload through the socket """
        if self.authenticator:
            payload = self.authenticator.signed(payload)
        self.sock.send(payload)

    def build_payload(self, tag, data):
        payload = bytes(tag.encode('utf-8')) + self.encode(data)
        return payload

    def publish(self, tag, data):
        """Publish a message"""
        payload = self.build_payload(tag, data)
        self.send(payload)
