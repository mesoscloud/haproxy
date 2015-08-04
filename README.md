# haproxy

[![Join the chat at https://gitter.im/mesoscloud/haproxy](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/mesoscloud/haproxy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

HAProxy

http://www.haproxy.org/

See https://github.com/mesoscloud/haproxy-marathon

## Ubuntu

[![](https://badge.imagelayers.io/mesoscloud/haproxy:1.5.14-ubuntu-14.04.svg)](https://imagelayers.io/?images=mesoscloud/haproxy:1.5.14-ubuntu-14.04)

e.g.

```
docker run -d
-e ZK=node-1:2181
--name=haproxy --net=host --restart=always mesoscloud/haproxy:1.5.14-ubuntu-14.04
```
