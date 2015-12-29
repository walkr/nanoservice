TODO
====

- Rewrite `process` of Subscriber and cleanup errors not thrown
- [ ] Add timeouts to prevent client.call to hang indefinitely
- [x] Rewrite service process routine for better reliability (e.g. do not explode if the encoder cannot encode the response).