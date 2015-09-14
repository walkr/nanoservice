"""Nanoservice encoders"""

import json
import logging
import msgpack


class Encoder(object):
    """Base encoder class"""

    # pylint: disable=unused-argument
    @classmethod
    def encode(cls, data):
        """Base encode function"""
        logging.error('Encoding fun not implemented')

    # pylint: disable=unused-argument
    @classmethod
    def decode(cls, data):
        """Base decode function"""
        logging.error('Decoding fun not implemented')


class JSONEncoder(Encoder):
    """Json encoder for nanoservice message"""
    def __init__(self):
        super(JSONEncoder, self).__init__()

    def encode(self, data):
        return json.dumps(data).encode('utf-8')

    def decode(self, data):
        return json.loads(data.decode('utf-8'))


class MsgPackEncoder(Encoder):
    """MsgPack encoder for nanoservice message"""
    def __init__(self):
        super(MsgPackEncoder, self).__init__()

    def encode(self, data):
        return msgpack.packb(data)

    def decode(self, data):
        return msgpack.unpackb(data, encoding='utf-8')
