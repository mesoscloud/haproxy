FROM centos:7
MAINTAINER Peter Ericson <pdericson@gmail.com>

RUN yum install -y epel-release && \
yum install -y gcc make openssl-devel pcre-devel python34 && \
curl -fLO https://bootstrap.pypa.io/get-pip.py && \
python3 get-pip.py && \
rm get-pip.py

RUN curl -fL http://www.haproxy.org/download/1.5/src/haproxy-1.5.17.tar.gz | tar xzf - -C /usr/src && \
make -C /usr/src/haproxy-1.5.17 TARGET=linux2628 USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1 && \
make -C /usr/src/haproxy-1.5.17 install && \
rm -rf /usr/src/haproxy-1.5.17

RUN pip3 install kazoo

RUN yum install -y openssl && mkdir -p /etc/haproxy

ENV HAPROXY_PEM /etc/haproxy/site.pem

COPY init.py /

CMD ["python3", "-u", "/init.py"]
