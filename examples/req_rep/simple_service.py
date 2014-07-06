import logging
from nanoservice import Service

def greet(name):
    return 'Hello {}'.format(name)

def add(x, y):
    return x+y

s = Service('ipc:///tmp/service.sock')
s.register('greet', greet)
s.register('add', add)
s.start()