# -*- coding: utf-8 -*-

import sys, os
from os.path import join, dirname 
location = join(dirname(sys.argv[0]), '..')

sys.path.insert(0, location)

import unittest
import FileObserver, FileMonitor

import os
import time

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO 

from sets import Set
from StringIO import StringIO
from FileTestHelper import FileTestHelper, msg_template

from FileMonitor import FileMonitor
from FileObserver import FileObserver
from Notifier import errorLabel, logLabel, infoLabel

class MockNotifier(object):
    """This class is meant for testing and simulates a GrowlNotifier"""
    def __init__(self):
        self.notifications = []
    def notify(self, notification, title, message, sticky):
        self.notifications.append((notification, title, message, sticky))

class FileObserverTest(unittest.TestCase, FileTestHelper):
    def setUp(self):
        self.mn = MockNotifier()
        self.fo = FileObserver(self.mn)
        self.fn1 = self.get_name()
        self.fn2 = self.get_name()
        self.log(self.fn1)
        self.log(self.fn1) # fn1/fn2 has messages starting from 3
        self.log(self.fn2) # the counter is unique, remember!
        self.fm1 = FileMonitor(self.fn1)
        self.fm2 = FileMonitor(self.fn2)
        
    def tearDown(self):
        os.unlink(self.fn1)
        os.unlink(self.fn2)
    
    def testEmpty(self):
        self.fo.register(self.fm1, True)
        self.fo.register(self.fm2, False)
        self.fo.alarm()
        
        self.assertEqual(self.mn.notifications, [])

    def testOneLine(self):
        self.fo.register(self.fm1)
        self.log(self.fn1)
        self.fo.alarm()
        self.assertEqual(self.mn.notifications, [(logLabel, self.fn1, msg_template % (4, self.fn1), False)])

    def testTwoLines(self):
        self.fo.register(self.fm1, True)
        self.fo.register(self.fm2, False)
        self.log(self.fn1)
        self.log(self.fn2)
        self.fo.alarm()
        self.assertEqual(self.mn.notifications,
                         [(logLabel, self.fn1, msg_template % (4, self.fn1), True),
                          (logLabel, self.fn2, msg_template % (5, self.fn2), False)])

    def testFalseAlarm(self):
        self.fo.register(self.fm1)
        self.fo.alarm()
        self.log(self.fn1)

        self.assertEqual(self.mn.notifications, [])
        self.fo.alarm()
        self.assertEqual(self.mn.notifications, [(logLabel, self.fn1, msg_template % (4, self.fn1), False) ])

    def testThreeLines(self):
        self.fo.register(self.fm1)
        self.fo.register(self.fm2)
        self.log(self.fn1)
        self.log(self.fn2)
        self.log(self.fn1)
        self.fo.alarm()
        
        self.assertEqual(Set(self.mn.notifications),
                         Set([(logLabel, self.fn1, msg_template % (4, self.fn1), False),
                          (logLabel, self.fn2, msg_template % (5, self.fn2), False),
                          (logLabel, self.fn1, msg_template % (6, self.fn1), False)]))
                          
    def testMoreEncodings(self):
        iso_8859_15_message = 'èéàò message\n'
        another_message = '\xa9 èéàò message\n'
        
        self.fo.register(self.fm1, True)
        self.log(self.fn1, iso_8859_15_message)
        self.log(self.fn1, another_message)
        self.fo.alarm()
        self.assertEqual(self.mn.notifications,
                         [(logLabel, self.fn1, iso_8859_15_message, True),
                          (logLabel, self.fn1, another_message, True)])
    
        
if __name__ == '__main__':
    unittest.main()
