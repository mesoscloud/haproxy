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
        cmd = ["haproxy", "-f", "/tmp/haproxy.cfg", "-p", "/tmp/haproxy.pid",
               "-sf", str(pid)]
    print("cmd:", ' '.join(cmd), file=sys.stderr)
    p = subprocess.Popen(cmd)
    r = p.wait()
    if r != 0:
        print("exit:", r, file=sys.stderr)


def main():

    host = os.getenv('HOST', '127.0.0.1')

    logging.basicConfig()

    mtime = 0
    zk = None
    while True:

        if os.path.exists('/tmp/haproxy.cfg'):
            haproxy_start()

        if zk is None:
            zk = kazoo.client.KazooClient(
                hosts=os.getenv('ZK', 'localhost:2181'), read_only=True)
            try:
                zk.start()
            except Exception as exc:
                print(str(exc.__class__.__name__) + ':', exc, file=sys.stderr)
                time.sleep(1)
                zk = None
                continue
        try:
            data, stat = zk.get("/haproxy/config")
        except kazoo.client.NoNodeError:
            print("No config", file=sys.stderr)
            time.sleep(10)
            continue
        except Exception as exc:
            print(str(exc.__class__.__name__) + ':', exc, file=sys.stderr)
            time.sleep(1)
            zk = None
            continue

        if mtime < stat.mtime:

            human = datetime.datetime.fromtimestamp(
                stat.mtime / 1000.0).ctime()

            print("version: %s, mtime: %s (%s)" %
                  (stat.version, stat.mtime, human),
                  file=sys.stderr)

            data = data.replace(b'bind 127.0.0.1:',
                                b'bind ' + host.encode('utf-8') + b':')

            with open('/tmp/haproxy.cfg', 'wb') as f:
                f.write(data)
            haproxy_start(restart=True)
            mtime = stat.mtime

        time.sleep(10)


if __name__ == '__main__':
    main()
