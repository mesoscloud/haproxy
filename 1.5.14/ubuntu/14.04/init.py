#!/usr/bin/python -u

"""HAProxy"""

import datetime
import logging
import os
import subprocess
import sys
import time

import kazoo.client


def pid():
    with open('/tmp/haproxy.pid') as f:
        return int(f.read().rstrip())


def main():
    logging.basicConfig()

    mtime = 0
    zk = None
    while True:

        if zk is None:
            zk = kazoo.client.KazooClient(hosts=os.getenv('ZK', '127.0.0.1:2181'), read_only=True)
        try:
            zk.start()
            data, stat = zk.get("/haproxy/config")
        except Exception as exc:
            print >>sys.stderr, str(exc.__class__.__name__) + ':', exc
            print >>sys.stderr, "Sleeping for 30 seconds..."
            time.sleep(30)
            zk = None
            continue

        if mtime < stat.mtime:

            print "mtime=%s (%s) version=%s" % (stat.mtime, datetime.datetime.fromtimestamp(stat.mtime / 1000.0).ctime(), stat.version)

            with open('/tmp/haproxy.cfg', 'w') as f:
                f.write(data)

            if os.path.exists('/tmp/haproxy.pid'):
                cmd = ["haproxy", "-f", "/tmp/haproxy.cfg", "-p", "/tmp/haproxy.pid", "-sf", str(pid())]
                print >>sys.stderr, "cmd:", ' '.join(cmd)
                p = subprocess.Popen(cmd)
            else:
                cmd = ["haproxy", "-f", "/tmp/haproxy.cfg", "-p", "/tmp/haproxy.pid"]
                print >>sys.stderr, "cmd:", ' '.join(cmd)
                p = subprocess.Popen(cmd)
            r = p.wait()
            if r != 0:
                print >>sys.stderr, "exit:", r

            print "pid:", pid()

            mtime = stat.mtime
        time.sleep(10)


if __name__ == '__main__':
    main()
