from nanoservice import Publisher


p = Publisher('ipc:///tmp/pubsub-service.sock')
p.publish('log_line', 'hello world')
p.publish('cap_line', 'this is uppercase')
