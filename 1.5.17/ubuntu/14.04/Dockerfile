FROM ubuntu:14.04
MAINTAINER Peter Ericson <pdericson@gmail.com>

RUN apt-get update && apt-get install --no-install-recommends -y curl gcc libpcre3-dev libssl-dev make python3 python3-pip && rm -rf /var/lib/apt/lists/*

RUN curl -fL http://www.haproxy.org/download/1.5/src/haproxy-1.5.17.tar.gz | tar xzf - -C /usr/src && \
make -C /usr/src/haproxy-1.5.17 TARGET=linux2628 USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1 && \
make -C /usr/src/haproxy-1.5.17 install && \
rm -rf /usr/src/haproxy-1.5.17

RUN pip3 install kazoo

RUN mkdir -p /etc/haproxy

ENV HAPROXY_PEM /etc/haproxy/site.pem

COPY init.py /

CMD ["python3", "-u", "/init.py"]
