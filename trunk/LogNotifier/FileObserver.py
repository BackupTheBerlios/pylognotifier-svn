#
#  $Id$
#  LogNotifier
#
#  Created by Riko on 23/10/06.
#  Copyright (c) 2006 Enrico Franchi. All rights reserved.
#

from Notifier import errorLabel, logLabel, infoLabel

def fileObserverFactory(notifier, preferenceModel):
    from FileMonitor import FileMonitor
    fo = FileObserver(notifier)
    for index in xrange(preferenceModel.numberOfEntries()):
        entry = preferenceModel.getEntryInfo(index)
        file_name = entry.file.encode('iso8859-15', 'replace')
        try: 
            fm = FileMonitor(entry.file)
            fo.register(fm, entry.sticky)
            notifier.notify(infoLabel, file_name, "Monitoring file")
        except IOError:
            notifier.notify(errorLabel, file_name, "No such file")
    return fo

class FileObserver(object):
    """Is an observer for file notifications.

    FileObserver(notifier)

    notifier is an object with a method notify(kind, title, description)
    they are supposed to be strings (however, this is not mandatory).
    This method is thought like that of GrowlNotifier, however, is general
    enough not to encapsulate it further, since a logger "notify" could have
    the very same signature whith kind one of error/warning/info and then
    a title: description thing.
    
    You add FileMonitors to be observed with register and remove them
    with register and unregister. In fact you may register every object that
    has an "is_modified()" method and that is iterable. Other operations are
    not performed
    """
    
    def __init__(self, notifier):
        self.files        = []
        self.notifier     = notifier
        self.sticky_flag  = []
        
    def register(self, f, sticky=False):
        self.files.append(f)
        self.sticky_flag.append(sticky)
        
    def unregister(self, f):
        c = self.files.count(f)
        if c > 0:
            self.files.remove(f)
            del self.sticky_flag[c]
        else: pass

    def alarm(self):
        for f, s in zip(self.files, self.sticky_flag):
            if f.is_modified():
                for line in f:
                    self.notifier.notify(logLabel, f.getName(), line, sticky=s)
