# Example service with authentication enabled

# Start service with a configuration file:
# > $ python auth_client.py auth_client.json

import sys
import time
import uuid
import random
import hashlib
import logging

from nanoservice import Responder
from nanoservice import Authenticator
from nanoservice import config


CONF = None


# *****************************************************
# SERVICE METHODS
# *****************************************************

def generate_uuid():
    """ Generate a random uuid """
    return uuid.uuid4().hex


# *****************************************************
# MAIN
# *****************************************************

def main():
    global CONF

    time.sleep(random.random())
    logging.basicConfig(level=logging.DEBUG)

    conf_filepath = sys.argv[1]
    CONF = config.load(conf_filepath)

    service = Responder(
        'ipc:///tmp/auth-example-service.sock',
        authenticator=Authenticator(
            CONF.authenticator['secret'], hashlib.sha256
        )
    )

    service.register('generate_uuid', generate_uuid)
    service.start()

if __name__ == '__main__':
    main()
