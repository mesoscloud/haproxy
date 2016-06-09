#!/usr/bin/env python

"""haproxy

The purpose of this script is to get haproxy config from zookeeper and
gracefully restart haproxy on config change.

"""

import logging
import os
import subprocess
import threading
import time

import kazoo.client
import kazoo.exceptions

CFG = '/tmp/haproxy.cfg'
PID = '/tmp/haproxy.pid'

logging.basicConfig()

lock = threading.Lock()


def call(cmd):
    """Log command invocation and exit status"""
    print("call:", ' '.join(cmd))
    print("exit:", subprocess.call(cmd))


def get_pid():
    """Get pid from PID, verify that the pid is not stale"""
    try:
        with open(PID) as f:
            pid = int(f.read())
        # This is a no-op signal
        os.kill(pid, 0)
        return pid
    except (FileNotFoundError, ProcessLookupError):
        pass


def main():
    host = os.getenv('HOST', '127.0.0.1')

    zk = kazoo.client.KazooClient(hosts=os.getenv('ZK', '127.0.0.1:2181'),
                                  read_only=True)
    # zk.start will raise an exception if zookeeper is not available,
    # this is recoverable if the restart policy for the container is
    # set to always.
    zk.start()

    @zk.DataWatch('/haproxy/config')
    def watch(data, stat):
        if data:
            print("version: {0.version}".format(stat))
        else:
            print("version: there is no config")
            return

        # replace bind 127.0.0.1 with the ip address of the private interface
        data = data.replace(b'bind 127.0.0.1:',
                            b'bind ' + host.encode('utf-8') + b':')

        with lock:
            with open(CFG, 'wb') as f:
                f.write(data)

            pid = get_pid()
            if pid:
                # restart haproxy
                call(['haproxy', '-f', CFG, '-p', PID, '-sf', str(pid)])
            else:
                call(['haproxy', '-f', CFG, '-p', PID])

    while True:
        with lock:
            if os.path.exists(CFG):
                # check that haproxy is running, it should be.
                pid = get_pid()
                if not pid:
                    call(['haproxy', '-f', CFG, '-p', PID])
        time.sleep(60)


if __name__ == '__main__':
    main()
