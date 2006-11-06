#
#  PreferenceModel.py
#  LogNotifier
#
#  Created by Riko on 23/10/06.
#  Copyright (c) 2006 Enrico Franchi. All rights reserved.
#

from CommonDefinitions import Log
from PreferenceBackend import preferenceBackendFactory

class EntryInfo(dict):
    """The EntryInfo class.
    
    It's a dictionary like object that allows to access members with dot
    notation.
    
    e = EntryInfo(hello='world')
    e["hello"] == e.hello
    """
    def __getattr__(self, key):
        return self[key]


class PreferenceModel(object):
    '''This class abstract preferences for LogNotifier
    
    It uses a PreferenceBackend object. It is created with preferenceBackendFactory.
    Inside that method we chose which kind of preferences to use.
    A PreferenceBackend acts as a dictionary
    '''
    def __init__(self, backend=None):
        if backend is None:
            self.backend = preferenceBackendFactory()
        else:
            self.backend = backend
        self.loadPreferences()
    
    def loadPreferences(self):
        '''Loads preferences from backend'''
        mf = self.backend[u"MonitoredFiles"]
        self.entries = [ EntryInfo(d) for d in mf]

    
    def savePreferences(self):    
        '''Cleans preferences and saves them to disk'''
        self._cleanPrefs()
        self.backend[u"MonitoredFiles"] = self.entries

    
    def getEntryInfo(self, row):
        '''Returns a tuple of values regarding a Log info
        
        For now only the first component is defined and is the Log name
        '''
        return self.entries[row]
    
    def setEntryInfo(self, row, d={}, **entry):
        try: e = self.entries[row]
        except IndexError: 
            e = EntryInfo()
            self.entries.append(e)
        e.update(d, **entry)
        
    def appendEntryInfo(self, d={}, **kargs):
        e = EntryInfo()
        e.update(d, **kargs)
        self.entries.append(e)

    def deleteEntryInfo(self, row):
        del self.entries[row]
        
    def numberOfEntries(self):
        return len(self.entries)
        
    def _cleanPrefs(self):
        '''We don't want to have duplicate files and empty files. It's a model babe! '''
        keys      = []
        to_remove = []
        # we have to decide if we want to support python2.3
        # otherwise we can use enumerate
        for index in xrange(len(self.entries)):
            entry = self.entries[index]
            if len(entry.file) == 0:
                to_remove.append(index)
            elif keys.count(entry.file):
                to_remove.append(index)
            else:
                keys.append(entry.file)
        for index in to_remove:
            del self.entries[index]