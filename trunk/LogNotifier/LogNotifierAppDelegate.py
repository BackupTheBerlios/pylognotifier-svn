#
#  LogNotifierAppDelegate.py
#  LogNotifier
#

from Foundation import *
from AppKit import *

from PyObjCTools import NibClassBuilder
from PreferenceModel import PreferenceModel
from Alarm import registerAlarm
from FileObserver import fileObserverFactory
from Notifier import notifierFactory
import Environment

PREFERENCES_CHANGED = 'RKLN_PreferencesChanged'

class LogNotifierAppDelegate(NibClassBuilder.AutoBaseClass):
    def init(self):        
        return self

    def awakeFromNib(self):
        pass
    
class RKLNTableViewDataSource(object):    
    def tableView_objectValueForTableColumn_row_(self, tableView, tableColumn, row):
        '''Gets the nth element.
        
        This method is needed for a dataSource'''
        e = self.getEntryInfo(row)        
        return e[tableColumn.identifier()]
    
    def tableView_setObjectValue_forTableColumn_row_(self, tableView, obj, tableColumn, row):
        '''Set's the nth element to...
        
        This method is needed for a dataSource'''
        if obj == u'' and tableColumn.identifier == u'file':
            self.deleteEntryInfo(row)
        else:
            self.setEntryInfo(row, {tableColumn.identifier():obj})
    
    def numberOfRowsInTableView_(self, tableView):
        '''Returns number of log files we have to check
        
        This method is needed for a dataSource'''
        return self.numberOfEntries()
        
        
# Warning: we have to verify if this is implementation dependent        
class PreferenceModel(PreferenceModel, RKLNTableViewDataSource):
    '''PreferenceModel is mixed in with RKLNTableViewDataSource.
    
    This could be considered kind of Python black magic.
    '''
    pass
    
class NotifierController(NibClassBuilder.AutoBaseClass):
    def awakeFromNib(self):
        NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(self, 
            'notifiyPreferencesChanged:', PREFERENCES_CHANGED, None)
        NSLog('NotificationController registered')
    def init(self):
        self.notifier = notifierFactory()
        self.fo       = fileObserverFactory(self.notifier, PreferenceModel())
        self.timer    = registerAlarm(self.fo)
        return self
        
    def notifiyPreferencesChanged_(self, notification):
        self._setPreferenceModel(PreferenceModel())
        
    def reloadPreferences_(self, sender):
        self._setPreferenceModel(PreferenceModel())

    def _setPreferenceModel(self, pm):
        self.timer.invalidate()
        self.fo    = fileObserverFactory(self.notifier, pm)
        self.timer = registerAlarm(self.fo)
    
    def __del__(self):
        NSNotificationCenter.defaultCenter().removeObserver_(self)        
    
class PreferenceManager(NibClassBuilder.AutoBaseClass):
    # the actual base class is NSObject
    # The following outlets are added to the class:
    # logList
    # window
    # applyButton

    def init(self):
        self.model = PreferenceModel()
        self.modified = False
        return self
         
    def loadPreferences_(self, sender):
        self.model.loadPreferences()
        self.modified = False
        self._updateUI()
                    
    def openWindow_(self, sender):
        self.window.makeKeyAndOrderFront_(self)
        self.loadPreferences_(sender)
        
    def savePreferences_(self, sender):
        self.model.savePreferences()
        self.modified = False
        NSNotificationCenter.defaultCenter().postNotificationName_object_userInfo_(
            PREFERENCES_CHANGED, self.model, None)
        self._updateUI()
        
    def cancel_(self, sender):
        self.window.orderOut_(self)
        
    def add_(self, sender):
        self.model.appendEntryInfo({u'file':'', u'sticky':False})
        self._updateUI()
        last_row_index = self.logList.numberOfRows() - 1
        self.logList.selectRowIndexes_byExtendingSelection_(
            NSIndexSet.indexSetWithIndex_(last_row_index), False)
        
    def remove_(self, sender):
        row = self.logList.selectedRow()
        if row >= 0:
            try:   self.model.deleteEntryInfo(row)
            except IndexError: pass
        self.modified = True
        self._updateUI()
        
    def tableView_objectValueForTableColumn_row_(self, tableView, tableColumn, row):
        return self.model.tableView_objectValueForTableColumn_row_(
                        tableView, tableColumn, row)
        
    def numberOfRowsInTableView_(self, tableView):
        return self.model.numberOfRowsInTableView_(tableView)
        
    def tableView_setObjectValue_forTableColumn_row_(self, tableView, obj, tableColumn, row):
        self.modified = True
        answ = self.model.tableView_setObjectValue_forTableColumn_row_(
                        tableView, obj, tableColumn, row)
        self._updateUI()
        return answ
        
    def _updateUI(self):
        self.applyButton.setEnabled_(self.modified)
        self.logList.reloadData()