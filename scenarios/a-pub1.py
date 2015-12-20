import time
from nanoservice import Publisher

name = 'pub1'
p = Publisher('ipc:///tmp/pub1.sock', bind=True)

while True:
    time.sleep(1)
    p.publish('log', 'Hello from {} at: {}'.format(name, time.time()))
