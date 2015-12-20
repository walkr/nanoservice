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

import json
import pickle
import logging
import msgpack


class Encoder(object):
    """ Base encoder class """

    # pylint: disable=unused-argument
    @classmethod
    def encode(cls, data):
        """ Base encode function """
        logging.error('Encoding fun not implemented')

    # pylint: disable=unused-argument
    @classmethod
    def decode(cls, data):
        """ Base decode function """
        logging.error('Decoding fun not implemented')


class JSONEncoder(Encoder):
    """ JSON encoder for nanoservice message """

    def __init__(self):
        super(JSONEncoder, self).__init__()

    def encode(self, data):
        return json.dumps(data).encode('utf-8')

    def decode(self, data):
        return json.loads(data.decode('utf-8'))


class MsgPackEncoder(Encoder):
    """ MsgPack encoder for nanoservice message """

    def __init__(self):
        super(MsgPackEncoder, self).__init__()

    def encode(self, data):
        return msgpack.packb(data)

    def decode(self, data):
        return msgpack.unpackb(data, encoding='utf-8')


class PickleEncoder(Encoder):
    """ Pickle encoder for nanoservice message """

    def __init__(self):
        super(PickleEncoder, self).__init__()

    def encode(self, data):
        return pickle.dumps(data)

    def decode(self, data):
        return pickle.loads(data)
