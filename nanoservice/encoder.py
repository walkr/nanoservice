import json
import logging
import msgpack


class Encoder(object):
    def encode(self, data):
        logging.error('Encoding fun not implemented')

    def decode(self, data):
        logging.error('Decoding fun not implemented')


class JSONEncoder(Encoder):
    def __init__(self):
        super(JSONEncoder, self).__init__()

    def encode(self, data):
        return json.dumps(data).encode('utf-8')

    def decode(self, data):
        return json.loads(data.decode('utf-8'))


class MsgPackEncoder(Encoder):
    def __init__(self):
        super(MsgPackEncoder, self).__init__()

    def encode(self, data):
        return msgpack.packb(data, use_bin_type=True)

    def decode(self, data):
        return msgpack.unpackb(data, encoding='utf-8')
