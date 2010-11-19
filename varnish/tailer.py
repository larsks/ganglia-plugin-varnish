#!/usr/bin/python

import os
import sys
import time
import errno
from stat import *

class ReopenFile(Exception):
    pass

class Tailer (object):
    '''This is a Python implementation of ``tail -f``.  This code will
    optionally continue to follow a file if it is replaced or truncated,
    which is useful when watching logfiles.'''

    def __init__ (self, pathname, interval=1,
            continue_if_missing=True,
            continue_if_replace=True,
            continue_if_truncate=True,
            replace_cb=None,
            truncate_cb=None):

        '''Create a new Tailer object for the specified pathname.
        
        Options:

        - ``continue_if_missing`` -- if True, periodically check to see if
          the file has been created and then start following it.  Otherwise
          it is an error if the file does not initially exist.

        - ``continue_if_replace`` -- if True, continue to follow a
          file when it is replaced (i.e., the inode changes.  Otherwise,
          stop following the file. Defaults to True

        - ``continue_if_truncate`` -- if True, continue to follow a
          file when it is truncated (the size changes in a negative
          direction).  Otherwise, stop following the file.  Defaults to
          True.

        - ``replace_cb`` -- if this is a callable, it will be called when
          the target file is replaced.

        - ``truncate_cb`` -- if this is a callable, it will be called when
          the target file is truncated.

        '''
        
        self.pathname = pathname
        self.interval = interval
        self.continue_if_missing = continue_if_missing
        self.continue_if_replace = continue_if_replace
        self.continue_if_truncate = continue_if_truncate
        self.last_inode = None

        self.truncate_cb = truncate_cb
        self.replace_cb = replace_cb

        self.following = False

    def open(self):
        self.fd = open(self.pathname)

        st_results = os.stat(self.pathname)
        st_inode = st_results[ST_INO]

        if not self.following:
            self.fd.seek(0, os.SEEK_END)

        self.last_inode = st_inode
        self.last_size = 0

    def __iter__(self):
        return self.follow()

    def check_file(self):
        '''Check to see if the target file has been replaced (inode has
        changed) or has been truncated (it got smaller).'''

        st_results = os.stat(self.pathname)
        st_size = st_results[ST_SIZE]
        st_inode = st_results[ST_INO]

        if st_inode != self.last_inode:
            # file has been replaced
            if callable(self.replace_cb):
                self.replace_cb(self)
            if self.continue_if_replace:
                raise ReopenFile()
            else:
                raise StopIteration()
        elif st_size < self.last_size:
            # file has been truncated
            if callable(self.truncate_cb):
                self.truncate_cb(self)
            if self.continue_if_truncate:
                raise ReopenFile()
            else:
                raise StopIteration()

        self.last_size = st_size

    def read_lines(self):
        '''Read lines from the file, periodically checking to see if
        the file has been replaced or truncated.'''

        while True:
            self.check_file()

            line = self.fd.readline()
            if not line:
                time.sleep(self.interval)
            else:
                yield(line)

    def initial_open(self):
        '''This is called when we first open the target file for reading.
        If the file does not exist and ``continue_if_missing`` is false, we
        pass on any exception from open().  If ``continue_if_missing`` is
        True, we loop until the file exists.'''

        while True:
            try:
                self.open()
                break
            except (OSError, IOError), detail:
                if detail.errno == errno.ENOENT \
                        and self.continue_if_missing:
                    self.following = True
                    time.sleep(self.interval)
                    continue
                
                raise

    def follow (self):
        '''Follow the target file.'''

        self.initial_open()

        while True:
            try:
                for line in self.read_lines():
                    yield line
            except (OSError, IOError), detail:
                if detail.errno == errno.ENOENT:
                    time.sleep(self.interval)
                    continue
            except ReopenFile:
                self.open()

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

