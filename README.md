[![Build Status](https://travis-ci.org/mesoscloud/haproxy.svg?branch=master)](https://travis-ci.org/mesoscloud/haproxy) [![Docker Stars](https://img.shields.io/docker/stars/mesoscloud/haproxy.svg)](https://hub.docker.com/r/mesoscloud/haproxy/) [![Docker Pulls](https://img.shields.io/docker/pulls/mesoscloud/haproxy.svg)](https://hub.docker.com/r/mesoscloud/haproxy/)

# haproxy

[![Join the chat at https://gitter.im/mesoscloud/mesoscloud](https://badges.gitter.im/mesoscloud/mesoscloud.svg)](https://gitter.im/mesoscloud/mesoscloud?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[HAProxy](http://www.haproxy.org/) is a tcp/http load balancer, the purpose of this image is to run haproxy with config from ZooKeeper, starting and reloading haproxy on config change with as close to zero client request interruption as possible.  A secondary goal is handle and recover from ZooKeeper outages without interrupting the haproxy process (and client requests).

The haproxy-marathon image is used to generate HAProxy config using Marathon as a data source (and storing the resulting config in ZooKeeper), see https://github.com/mesoscloud/haproxy-marathon

## CentOS

[![](https://badge.imagelayers.io/mesoscloud/haproxy:1.5.17-centos-7.svg)](https://imagelayers.io/?images=mesoscloud/haproxy:1.5.17-centos-7)

e.g.

```
docker run -d \
-e ZK=node-1:2181 \
--name=haproxy --net=host --restart=always mesoscloud/haproxy:1.5.17-centos-7
```

## Ubuntu

[![](https://badge.imagelayers.io/mesoscloud/haproxy:1.5.17-ubuntu-14.04.svg)](https://imagelayers.io/?images=mesoscloud/haproxy:1.5.17-ubuntu-14.04)

e.g.

```
docker run -d \
-e ZK=node-1:2181 \
--name=haproxy --net=host --restart=always mesoscloud/haproxy:1.5.17-ubuntu-14.04
```
