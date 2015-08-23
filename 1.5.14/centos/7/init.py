#!/usr/bin/python -u
#
# Copyright (c) 2015 Peter Ericson <pdericson@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

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
    print("cmd:", ' '.join(cmd), file=sys.stderr)
    p = subprocess.Popen(cmd)
    r = p.wait()
    if r != 0:
        print("exit:", r, file=sys.stderr)


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
            print(str(exc.__class__.__name__) + ':', exc, file=sys.stderr)
            print("Sleeping for 30 seconds...", file=sys.stderr)
            time.sleep(30)
            zk = None
            continue

        if mtime < stat.mtime:
            print("version: %s, mtime: %s (%s)" % (stat.version, stat.mtime, datetime.datetime.fromtimestamp(stat.mtime / 1000.0).ctime()), file=sys.stderr)
            with open('/tmp/haproxy.cfg', 'wb') as f:
                f.write(data)
            haproxy_start(restart=True)
            mtime = stat.mtime

        time.sleep(10)


if __name__ == '__main__':
    main()
