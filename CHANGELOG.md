Changelog
=========

### Current

* Rewrote process method of Subscriber

### 0.5.0

* Part of service module were rewritten, so that it does not explode when
  failing to decode a request
* Better testing


### 0.4.1

* Improve authenticator performance


### 0.4.0

* Rename Service and Client `recv` method to `receive`
* Add crypto module
* Add optional message authentication between endpoints
* PubSub logic moved to a new module
* PubClient renamed to Publisher
* SubService renamed to Subscriber

### 0.1.0

* Initial release