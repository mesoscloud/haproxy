FROM mesoscloud/ubuntu:14.04-20160605
MAINTAINER Peter Ericson <pdericson@gmail.com>

# install python3 and kazoo, compile haproxy
RUN HAPROXY_VERSION=1.5.14; \
\
apt-get update && \
apt-get install --no-install-recommends -y curl gcc libpcre3-dev libssl-dev make python3 python3-pip && \
rm -rf /var/lib/apt/lists/* && \
\
pip3 install kazoo && \
\
curl -fL http://www.haproxy.org/download/1.5/src/haproxy-$HAPROXY_VERSION.tar.gz | tar xzf - -C /usr/src && \
make -C /usr/src/haproxy-$HAPROXY_VERSION TARGET=linux2628 USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1 && \
make -C /usr/src/haproxy-$HAPROXY_VERSION install && \
rm -rf /usr/src/haproxy-$HAPROXY_VERSION

COPY init.py /

CMD ["python3", "-u", "/init.py"]
