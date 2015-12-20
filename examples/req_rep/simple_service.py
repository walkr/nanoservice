import logging
from nanoservice import Responder


def greet(name):
    return 'Hello {}'.format(name)


def add(x, y):
    return x + y

s = Responder('ipc:///tmp/service.sock')
s.register('greet', greet)
s.register('add', add)
s.start()
