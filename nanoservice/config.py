""" Read configuration for a service from a json file """

import io
import re
import json

from .client import Client


class DotDict(dict):
    """ Access a dictionary like an object """

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


def load(filepath=None, filecontent=None, clients=True):
    """ Read the json file located at `filepath`

    If `filecontent` is specified, its content will be json decoded
    and loaded instead. The `clients` arg is a binary flag
    which specifies whether the endpoints present in config (`filecontent`),
    should be used to create `Client` objects.

    Usage:
        config.load(filepath=None, filecontent=None):
        Provide either a filepath or a json string
    """
    conf = DotDict()

    # Read json configuration
    assert filepath or filecontent
    if not filecontent:
        with io.FileIO(filepath) as fh:
            filecontent = fh.read().decode('utf-8')
    configs = json.loads(filecontent)

    # Update the conf items (Create clients if necessary)
    for key, value in configs.items():
        conf[key] = value
        if clients and re.match('inproc:|ipc:|tcp:', value):
            conf[key] = Client(value)
    return conf
