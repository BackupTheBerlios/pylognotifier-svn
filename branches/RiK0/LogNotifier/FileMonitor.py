#
#  FileMonitor.py
#  LogNotifier
#
#  Created by Riko on 23/10/06.
#  Copyright (c) 2006 Enrico Franchi. All rights reserved.
#

import os, codecs

def is_filelike(f):
    return hasattr(f, 'readline')
    
def is_file(f):
    return hasattr(f, 'fileno')

class FileMonitor(object):
    def __init__(self, f):
        if is_file(f):
            self._file = codecs.EncodedFile(f, 'iso8859-15', errors='replace')
            self.name = f.name
        else:
            self.name = f
            self._file = codecs.open(f, encoding='iso8859-15', errors='replace')
        self._position_to_end()
        self.update()

    def size(self):
        return os.fstat(self.fileno()).st_size
        
    def mtime(self):
        return os.fstat(self.fileno()).st_mtime

    def is_modified(self):
        return (self.size() != self._size) or (self.mtime() != self._mtime)

    def fileno(self):
        return self._file.fileno()

#    def read(self, n=-1):
#        return self._file.read(n)
        
    def readline(self, sz=-1):
        buf = self._file.readline(sz)
        if self._file.tell() == self.size(): self.update()
        return buf

    def _position_to_end(self):
        self._file.seek(0, 2)
        self.update()
        
    def update(self):
        st = os.fstat(self.fileno()) # this is done for performance reasons
        self._size  = st.st_size
        self._mtime = st.st_mtime

    def __iter__(self):
        while self.is_modified():
            yield self.readline()

