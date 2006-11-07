# -*- coding: iso8859-15 -*-
#
#  test_FileMonitor.py
#  LogNotifier
#
#  Created by Riko on 23/10/06.
#  Copyright (c) 2006 __MyCompanyName__. All rights reserved.
#

import sys, os
from os.path import join, dirname 
location = join(dirname(sys.argv[0]), '..')

sys.path.insert(0, location)

import unittest
import FileMonitor

import time

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO 
    
from StringIO import StringIO

from FileTestHelper import FileTestHelper

class FileMonitorTest(unittest.TestCase, FileTestHelper):
    
    def setUp(self):
        self.fname = self.get_name()
        self.counter = 1
        for i in xrange(3): self.log(self.fname)
            
    def tearDown(self):
        # os.system('/usr/local/bin/mate -w %s' % self.fname)
        os.unlink(self.fname)

    def testIsFileLike(self):
        self.assert_(FileMonitor.is_filelike(file(sys.argv[0])))
        self.assert_(FileMonitor.is_filelike(StringIO()))

    def testEmpty(self):
        fm = FileMonitor.FileMonitor(self.fname)
        self.failIf(fm.is_modified())
        self.assertEqual(fm.readline(), '')
            
    def testOneLine(self):
        fm = FileMonitor.FileMonitor(self.fname)
        self.log(self.fname)
        self.assert_(fm.is_modified())
        self.assertEqual(fm.readline(), "Message no 4 file %s\n" % self.fname)
        self.failIf(fm.is_modified())
    
    def testTwoLines(self):
        fm = FileMonitor.FileMonitor(self.fname)
        self.failIf(fm.is_modified())
        self.log(self.fname)
        self.log(self.fname)
        self.assert_(fm.is_modified())
        print fm.size(), fm._size
        print fm.mtime(), fm._mtime
        print fm._file.tell()
        import pdb 
        pdb.set_trace()
        self.assertEqual(fm.readline(), "Message no 4 file %s\n" % self.fname)
        print fm._file.tell()
        print fm.size(), fm._size
        print fm.mtime(), fm._mtime
        #self.assert_(fm.is_modified())
        self.assertEqual(fm.readline(), "Message no 5 file %s\n" % self.fname)
        self.failIf(fm.is_modified())
    
    def testInterleavedLines(self):
        fm = FileMonitor.FileMonitor(self.fname)
        self.failIf(fm.is_modified())
        self.log(self.fname)
        self.assert_(fm.is_modified())
        self.assertEqual(fm.readline(), "Message no 4 file %s\n" % self.fname)
        self.failIf(fm.is_modified())
        self.log(self.fname)
        self.assert_(fm.is_modified())
        self.assertEqual(fm.readline(), "Message no 5 file %s\n" % self.fname)
        self.failIf(fm.is_modified())
        
    def testEncodings(self):
        fm = FileMonitor.FileMonitor(self.fname)
        self.log(self.fname, "Hello, è char\n")
        self.assert_(fm.is_modified())
        self.assertEqual(fm.readline(), "Hello, è char\n")
        self.log(self.fname, "Hello ©\n")
        self.assert_(fm.is_modified())
        line = fm.readline()
        self.assertEqual(line, "Hello ©\n")
        
if __name__ == '__main__':
    unittest.main()
