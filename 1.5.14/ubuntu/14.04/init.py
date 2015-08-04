#!/usr/bin/python -u

"""HAProxy"""

import logging
import os
import subprocess
import sys
import time

import kazoo.client


def main():
    logging.basicConfig()

    zk = kazoo.client.KazooClient(hosts=os.getenv('ZK', '127.0.0.1:2181'), read_only=True)
    zk.start()

    mtime = 0
    while True:
        data, stat = zk.get("/haproxy/config")
        if mtime < stat.mtime:

            with open('/tmp/haproxy.cfg', 'w') as f:
                f.write(data)

            if os.path.exists('/tmp/haproxy.pid'):
                with open('/tmp/haproxy.pid') as f:
                    pid = f.read().rstrip()
                print >>sys.stderr, "start (reload)"
                p = subprocess.Popen(["haproxy", "-f", "/tmp/haproxy.cfg", "-p", "/tmp/haproxy.pid", "-sf", pid])
            else:
                print >>sys.stderr, "start"
                p = subprocess.Popen(["haproxy", "-f", "/tmp/haproxy.cfg", "-p", "/tmp/haproxy.pid"])
            p.wait()

            mtime = stat.mtime
        time.sleep(10)


if __name__ == '__main__':
    main()
