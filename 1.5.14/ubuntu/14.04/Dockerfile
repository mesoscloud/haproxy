FROM ubuntu:14.04

RUN apt-get update && apt-get install -y curl gcc libpcre3-dev libssl-dev make python python-pip

RUN curl -fL http://www.haproxy.org/download/1.5/src/haproxy-1.5.14.tar.gz | tar xzf - -C /usr/src && \
cd /usr/src/haproxy-1.5.14 && \
make TARGET=linux2628 USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1 && \
make install && \
cd .. && \
rm -rf /usr/src/haproxy-1.5.14

RUN pip install kazoo

COPY init.py /

CMD ["/init.py"]
