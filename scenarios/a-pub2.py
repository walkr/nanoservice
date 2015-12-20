import time
from nanoservice import Publisher

name = 'pub2'
p = Publisher('ipc:///tmp/pub2.sock', bind=True)

while True:
    time.sleep(1)
    p.publish('log', 'Hello from {} at: {}'.format(name, time.time()))
