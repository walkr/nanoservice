nanoservice
===========
nanoservice is a small Python library for writing lightweight networked services
using [nanomsg](http://nanomsg.org/)

Using nanoservice you can break up monolithic applications into small,
specialized services which communicate with each other.


## Install

From project directory

```shell
$ make install
```

Or via pip

```shell
$ pip install nanoservice
```


### Example


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


[*] Check out examples directory for more examples.
