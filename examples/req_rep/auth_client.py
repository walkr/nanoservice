import time
import hashlib

from nanoservice import Requester
from nanoservice import Authenticator


def main():
    c = Requester(
        'ipc:///tmp/auth-example-service.sock',
        authenticator=Authenticator('my-super-secret', hashlib.sha256)
    )

    n = 100
    started = time.time()
    for i in range(n):
        _, err = c.call('generate_uuid')
        assert err is None

    duration = time.time() - started
    print(
        'Generated {} uuids in {:.3f} secs. ({:.2f} uuid/sec)'
        .format(n, duration, n / duration)
    )


if __name__ == '__main__':
    main()
