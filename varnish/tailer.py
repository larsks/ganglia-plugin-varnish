#!/usr/bin/python

import os
import sys
import time
import errno
from stat import *

class ReopenFile(Exception):
    pass

class Tailer (object):

    def __init__ (self, pathname, interval=1,
            continue_on_replace=True,
            continue_on_truncate=True,
            replace_cb=None,
            truncate_cb=None):
        
        self.pathname = pathname
        self.interval = interval
        self.continue_on_replace = continue_on_replace
        self.continue_on_truncate = continue_on_truncate
        self.last_inode = None

        self.truncate_cb = truncate_cb
        self.replace_cb = replace_cb

    def open(self):
        self.fd = open(self.pathname)

        st_results = os.stat(self.pathname)
        st_inode = st_results[ST_INO]

        if self.last_inode is None:
            self.fd.seek(0, os.SEEK_END)

        self.last_inode = st_inode
        self.last_size = 0

    def __iter__(self):
        return self.follow()

    def check_file(self):
        st_results = os.stat(self.pathname)
        st_size = st_results[ST_SIZE]
        st_inode = st_results[ST_INO]

        if st_inode != self.last_inode:
            # file has been replaced
            if callable(self.replace_cb):
                self.replace_cb(self)
            if self.continue_on_replace:
                raise ReopenFile()
            else:
                raise StopIteration()
        elif st_size < self.last_size:
            # file has been truncated
            if callable(self.truncate_cb):
                self.truncate_cb(self)
            if self.continue_on_truncate:
                raise ReopenFile()
            else:
                raise StopIteration()

        self.last_size = st_size

    def read_lines(self):
        while True:
            self.check_file()

            where = self.fd.tell()
            line = self.fd.readline()
            if not line:
                time.sleep(self.interval)
                self.fd.seek(where)
            else:
                yield(line)

    def follow (self):
        while True:
            self.open()

            try:
                for line in self.read_lines():
                    yield line
            except (OSError, IOError), detail:
                if detail.errno == errno.ENOENT:
                    time.sleep(self.interval)
                    continue
            except ReopenFile:
                continue

def event_logger(msg):
    def _ (t):
        print >>sys.stderr, msg % t.pathname

    return _

if __name__ == '__main__':

    import sys
    for line in Tailer(sys.argv[1], 
            replace_cb=event_logger('REPLACED: %s'),
            truncate_cb=event_logger('TRUNCATE: %s')):
        print 'LINE:', line,

