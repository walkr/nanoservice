from nanoservice import Subscriber


def log(message):
    print('Subscriber got new message: {}'.format(message))

s = Subscriber('ipc:///tmp/pub1.sock', bind=False)
s.socket.connect('ipc:///tmp/pub2.sock')
s.subscribe('log', log)
s.start()
