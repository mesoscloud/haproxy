# haproxy

[![Join the chat at https://gitter.im/mesoscloud/haproxy](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/mesoscloud/haproxy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[HAProxy](http://www.haproxy.org/) is a tcp/http load balancer, the purpose of this image is to run haproxy with config from ZooKeeper, starting and reloading haproxy on config change with as close to zero client request interruption as possible.  A secondary goal is handle and recover from ZooKeeper outages without interrupting the haproxy process (and client requests).

The haproxy-marathon image is used to generate HAProxy config using Marathon as a data source (and storing the resulting config in ZooKeeper), see https://github.com/mesoscloud/haproxy-marathon

## CentOS

[![](https://badge.imagelayers.io/mesoscloud/haproxy:1.5.14-centos-7.svg)](https://imagelayers.io/?images=mesoscloud/haproxy:1.5.14-centos-7)

e.g.

```
docker run -d \
-e ZK=node-1:2181 \
--name=haproxy --net=host --restart=always mesoscloud/haproxy:1.5.14-centos-7
```

## Ubuntu

[![](https://badge.imagelayers.io/mesoscloud/haproxy:1.5.14-ubuntu-14.04.svg)](https://imagelayers.io/?images=mesoscloud/haproxy:1.5.14-ubuntu-14.04)

e.g.

```
docker run -d \
-e ZK=node-1:2181 \
--name=haproxy --net=host --restart=always mesoscloud/haproxy:1.5.14-ubuntu-14.04
```
