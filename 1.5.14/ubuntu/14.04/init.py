#!/usr/bin/python -u

"""HAProxy"""

import datetime
import logging
import os
import subprocess
import sys
import time

import kazoo.client


def haproxy_pid():
    """Return pid of haproxy or None if haproxy is not running"""
    if os.path.exists('/tmp/haproxy.pid'):
        with open('/tmp/haproxy.pid') as f:
            pid = int(f.read().rstrip())
        try:
            os.kill(pid, 0)
        except OSError:
            return
        return pid


def haproxy_start(restart=False):
    """Start or restart haproxy, do not restart haproxy if restart is False"""
    pid = haproxy_pid()
    if pid is None:
        cmd = ["haproxy", "-f", "/tmp/haproxy.cfg", "-p", "/tmp/haproxy.pid"]
    else:
        if not restart:
            return
        cmd = ["haproxy", "-f", "/tmp/haproxy.cfg", "-p", "/tmp/haproxy.pid", "-sf", str(pid)]
    print >>sys.stderr, "cmd:", ' '.join(cmd)
    p = subprocess.Popen(cmd)
    r = p.wait()
    if r != 0:
        print >>sys.stderr, "exit:", r


def main():
    logging.basicConfig()

    mtime = 0
    zk = None
    while True:

        if os.path.exists('/tmp/haproxy.cfg'):
            haproxy_start()

        if zk is None:
            zk = kazoo.client.KazooClient(hosts=os.getenv('ZK', 'localhost:2181'), read_only=True)
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
            print >>sys.stderr, "version: %s, mtime: %s (%s)" % (stat.version, stat.mtime, datetime.datetime.fromtimestamp(stat.mtime / 1000.0).ctime())
            with open('/tmp/haproxy.cfg', 'w') as f:
                f.write(data)
            haproxy_start(restart=True)
            mtime = stat.mtime

        time.sleep(10)


if __name__ == '__main__':
    main()
