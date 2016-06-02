FROM ubuntu:14.04
MAINTAINER Peter Ericson <pdericson@gmail.com>

RUN apt-get update && apt-get install --no-install-recommends -y curl gcc libpcre3-dev libssl-dev make python3 python3-pip && rm -rf /var/lib/apt/lists/*

# https://github.com/Yelp/dumb-init
RUN curl -fLsS -o /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.0.2/dumb-init_1.0.2_amd64 && chmod +x /usr/local/bin/dumb-init

RUN curl -fL http://www.haproxy.org/download/1.5/src/haproxy-1.5.17.tar.gz | tar xzf - -C /usr/src && \
make -C /usr/src/haproxy-1.5.17 TARGET=linux2628 USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1 && \
make -C /usr/src/haproxy-1.5.17 install && \
rm -rf /usr/src/haproxy-1.5.17

RUN pip3 install kazoo

COPY init.py /

ENTRYPOINT ["/usr/local/bin/dumb-init"]

CMD ["python3", "-u", "/init.py"]
