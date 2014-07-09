nanoservice
===========
nanoservice is a small Python library for writing lightweight networked services
using [nanomsg](http://nanomsg.org/)

With nanoservice you can break up monolithic applications into small,
specialized services which communicate with each other.

[![Build Status](https://travis-ci.org/walkr/nanoservice.svg?branch=master)](https://travis-ci.org/walkr/nanoservice)

## Install

1) Make sure you have the nanomsg library installed:

```shell
$ git clone git@github.com:nanomsg/nanomsg.git
$ ./configure
$ make
$ make check
$ sudo make install
```

For more details visit the official [nanomsg repo](https://github.com/nanomsg/nanomsg)

On OS X you can also do:

```shell
$ brew install nanomsg
```

2) Install nanoservice:

From project directory

```shell
$ make install
```

Or via pip

```shell
$ pip install nanoservice (it's broken)
```


## Example Usage


The service:

```python
from nanoservice import Service

def echo(msg):
    return msg

s = Service('ipc:///tmp/service.sock')
s.register('echo', echo)
s.start()
```


```shell
$ python echo_service.py
```

The client:

```python
from nanoservice import Client

c = Client('ipc:///tmp/service.sock')
res, err = c.call('echo', 'hello world’)
print('Result is {}'.format(res))
```

```shell
$ python my_client.py
$ Result is: hello world
```

## Other

To run tests:

```shell
$ make test
```

To run benchmarks

```shell
$ make bench
```

Check out examples directory for more examples.

MIT Licensed
