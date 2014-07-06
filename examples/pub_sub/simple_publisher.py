# client

from nanoservice import PubClient

c = PubClient('ipc:///tmp/pubsub-service.sock')
c.publish('log_line', 'hello world')
c.publish('cap_line', 'this is uppercase')

