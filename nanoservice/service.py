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

import nanomsg
import logging

from .encoder import MsgPackEncoder
from .error import ServiceError


class Service(object):

    def __init__(self, addr, encoder=None, socket=None):
        self.addr = addr
        self.encoder = encoder or MsgPackEncoder()
        self.methods = {}
        self.sock = socket if socket else nanomsg.Socket(nanomsg.REP)
        self.sock.bind(self.addr)

    def recv(self):
        payload = self.sock.recv()
        decoded = self.encoder.decode(payload)
        return decoded

    def send(self, response):
        response = self.encoder.encode(response)
        self.sock.send(response)

    def execute(self, method, args, ref):
        response = {'result': None, 'error': None, 'ref': ref}

        # Execute the requested method
        fun = self.methods.get(method)
        if not fun:
            response['error'] = 'Method `{}` not found'.format(method)
        else:
            try:
                response['result'] = fun(*args)
            except Exception as e:
                logging.error(e, exc_info=1)
                response['error'] = str(e)
        return response

    def register(self, name, fun):
        self.methods[name] = fun

    def process(self):
        payload = self.recv()
        logging.debug(
            '* Server received payload: {}'.format(payload))
        try:
            method, args, ref = payload
            response = self.execute(method, args, ref)
        except Exception as e:
            logging.error(e, exc_info=1)
        else:
            self.send(response)

    def start(self):
        """ Start and listen for calls """

        logging.info('* Service started on {}'.format(self.addr))
        while True:
            self.process()


class SubService(Service):
    """ A service which subscribes """

    def __init__(self, addr, encoder=None):
        socket = nanomsg.Socket(nanomsg.SUB)
        super(SubService, self).__init__(addr, encoder, socket)

    def get_fun_and_data(self, msg):
        for name in self.methods:
            tag = bytes(name.encode('utf-8'))
            if msg.startswith(tag):
                fun = self.methods.get(name)
                data = self.encoder.decode(msg[len(tag):])
                return fun, data
        return None, None

    def register(self, name, fun):
        raise ServiceError('Operation not allowed on this type of service')

    def subscribe(self, name, fun):
        super(SubService, self).register(name, fun)
        self.sock.set_string_option(nanomsg.SUB, nanomsg.SUB_SUBSCRIBE, name)

    def process(self):
        msg = self.sock.recv()
        fun, data = self.get_fun_and_data(msg)

        result = None
        try:
            result = fun(data)
        except Exception as e:
            logging.error(e, exc_info=1)

        # Return result to check successful execution
        # of `fun` when testing
        return result
