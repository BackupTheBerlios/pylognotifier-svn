import sys, os, unittest
from os.path import join, dirname 
location = join(dirname(sys.argv[0]), '..')

sys.path.insert(0, location)

import PreferenceModel
from PreferenceModel import PreferenceModel

import time

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO 
    
from StringIO import StringIO
from FileTestHelper import FileTestHelper
from sets import Set


class PreferenceModelTest(unittest.TestCase):
    def setUp(self):
        self.defaultValues = {
            'MonitoredFiles' :[
                  { 'file'   : '/var/log/system.log',
                    'sticky' : True},
                  { 'file'   : '/var/log/console.log',
                    'sticky' : False}
            ]
        }

        self.pm = PreferenceModel(self.defaultValues)
        
    def testDoesNotModify(self):
        d = {'MonitoredFiles':[{'file':'afile', 'sticky':False}, ]}
        pm = PreferenceModel(d)
        self.assertEqual(pm.getEntryInfo(0).file, 'afile')
        
    def testModifyAFile(self):
        self.pm.setEntryInfo(0, {'file':'var/hello.log', 'sticky':False}) # note the missing /
        self.assertEqual(self.pm.getEntryInfo(0).file, 'var/hello.log')
        self.assertEqual(self.pm.getEntryInfo(1).file, '/var/log/console.log')
        self.pm.savePreferences()
        self.assertEqual(self.defaultValues, 
            {
                'MonitoredFiles' :[
                      { 'file'   : 'var/hello.log',
                        'sticky' : False},
                      { 'file'   : '/var/log/console.log',
                        'sticky' : False}
                ]
            }
        
        )
        

    def testAddEntry(self):
        self.pm.setEntryInfo(2, {'file':'/var/log/another.log', 'sticky':False})
        self.assertEqual(self.pm.getEntryInfo(0).file, '/var/log/system.log')
        self.assertEqual(self.pm.getEntryInfo(1).file, '/var/log/console.log')
        self.assertEqual(self.pm.getEntryInfo(2).file, '/var/log/another.log')
        self.pm.savePreferences()
        self.assertEqual(self.defaultValues, 
            {
                'MonitoredFiles' :[
                      { 'file'   : '/var/log/system.log',
                        'sticky' : True},
                      { 'file'   : '/var/log/console.log',
                        'sticky' : False},
                      { 'file'   : '/var/log/another.log',
                        'sticky' : False}
                ]
            }

        )

    def testRemoveEntry(self):
        self.pm.deleteEntryInfo(0)
        self.assertEqual(self.pm.getEntryInfo(0).file, '/var/log/console.log')
        self.assertRaises(IndexError, self.pm.getEntryInfo, 1)
        self.pm.savePreferences()
        self.assertEqual(self.defaultValues, 
            {
                'MonitoredFiles' :[
                      { 'file'   : '/var/log/console.log',
                        'sticky' : False}
                ]
            }
        )
        
    def testCleaningRemoveDoubleNames(self):
        self.pm.setEntryInfo(2, {'file':'/var/log/system.log', 'sticky':False}) # note the missing /
        self.assertEqual(self.pm.getEntryInfo(0).file,   '/var/log/system.log')
        self.assertEqual(self.pm.getEntryInfo(1).file,   '/var/log/console.log')
        self.assertEqual(self.pm.getEntryInfo(2).file,   '/var/log/system.log')
        self.assertEqual(self.pm.getEntryInfo(0).sticky, True)
        self.assertEqual(self.pm.getEntryInfo(2).sticky, False)
        self.pm.savePreferences()
        self.assertEqual(self.defaultValues, 
            {
                'MonitoredFiles' :[
                      { 'file'   : '/var/log/system.log',
                        'sticky' : True},
                      { 'file'   : '/var/log/console.log',
                        'sticky' : False}
                ]
            }
        )
        
    def testVoidNameRemoves(self):
        self.pm.setEntryInfo(1, file='')
        self.assertEqual(self.pm.getEntryInfo(0).file,   '/var/log/system.log')
        self.assertEqual(self.pm.getEntryInfo(1).file,   '')
        self.assertEqual(self.pm.getEntryInfo(0).sticky, True)
        self.assertEqual(self.pm.getEntryInfo(1).sticky, False)
        self.pm.savePreferences()
        self.pm.loadPreferences()
        self.assertEqual(self.pm.getEntryInfo(0).file,   '/var/log/system.log')
        self.assertRaises(IndexError, self.pm.getEntryInfo, 1)
        self.assertEqual(self.defaultValues, 
            {
                'MonitoredFiles' :[
                      { 'file'   : '/var/log/system.log',
                        'sticky' : True}
                ]
            }
        )
        
    def testLoadPreferencesDiscardsState(self):
        self.pm.setEntryInfo(2, {'file':'/var/log/another.log', 'sticky':False})
        self.assertEqual(self.pm.getEntryInfo(0).file, '/var/log/system.log')
        self.assertEqual(self.pm.getEntryInfo(1).file, '/var/log/console.log')
        self.assertEqual(self.pm.getEntryInfo(2).file, '/var/log/another.log')
        self.pm.loadPreferences()
        self.assertRaises(IndexError, self.pm.getEntryInfo, 2)
        self.assertEqual(self.defaultValues, 
            {
                'MonitoredFiles' :[
                      { 'file'   : '/var/log/system.log',
                        'sticky' : True},
                      { 'file'   : '/var/log/console.log',
                        'sticky' : False}
                ]
            }
        )
        
    def testAddEntryWithAppend(self):
        self.pm.appendEntryInfo({'file':'/var/log/another.log', 'sticky':False})
        self.pm.appendEntryInfo(file='/var/log/athirdone.log', sticky=False)
        self.pm.appendEntryInfo(file='', sticky=False)
        self.assertEqual(self.pm.getEntryInfo(0).file, '/var/log/system.log')
        self.assertEqual(self.pm.getEntryInfo(1).file, '/var/log/console.log')
        self.assertEqual(self.pm.getEntryInfo(2).file, '/var/log/another.log')
        self.assertEqual(self.pm.getEntryInfo(3).file, '/var/log/athirdone.log')
        self.assertEqual(self.pm.getEntryInfo(4).file, '')
        self.pm.savePreferences()
        self.assertEqual(self.defaultValues, 
            {
                'MonitoredFiles' :[
                      { 'file'   : '/var/log/system.log',
                        'sticky' : True},
                      { 'file'   : '/var/log/console.log',
                        'sticky' : False},
                      { 'file'   : '/var/log/another.log',
                        'sticky' : False},
                      { 'file'   : '/var/log/athirdone.log',
                        'sticky' : False},
                        
                ]
            }

        )
        
if __name__ == '__main__':
    unittest.main()
