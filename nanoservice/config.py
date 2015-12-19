""" Read configuration for a service from a json file """

import io
import json


class DotDict(dict):
    """ Access a dictionary like an object """

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


def load(filepath=None, filecontent=None):
    """ Read the json file located at `filepath`

    If `filecontent` is specified, its content will be json decoded
    and loaded instead.

    Usage:
        config.load(filepath=None, filecontent=None):
        Provide either a filepath or a json string
    """
    conf = DotDict()

    assert filepath or filecontent
    if not filecontent:
        with io.FileIO(filepath) as handle:
            filecontent = handle.read().decode('utf-8')
    configs = json.loads(filecontent)
    conf.update(configs.items())
    return conf
