# Redis Sharding

## Table of contents
- [General Description](#general-description)
- [Issues](#issues)

## General Description
Redis' synchronous nature combined with large, hulking datasets that need to be scanned repeatedly and often make for poor scalability. Let's mitigate those bottlenecks by splitting up the data Redis has to scan across databases, and entire threads of execution across instances.

## Issues

- [`rb`](https://github.com/getsentry/rb) package [has a `redis` requirement < 3.5](https://github.com/getsentry/rb/blob/6f96a68dca2d77e9ac1d8bdd7a21e2575af65a20/setup.py#L15)
