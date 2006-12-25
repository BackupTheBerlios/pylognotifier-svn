#
#  PreferenceBackend.py
#  LogNotifier
#
#  Created by Riko on 23/10/06.
#  Copyright (c) 2006 Enrico Franchi. All rights reserved.
#

def preferenceBackendFactory():
    try:
        import Foundation
        return CocoaPreferenceBackend()
    except ImportError:
        raise 

class CocoaPreferenceBackend(object):
    """The CocoaPreferenceBackend class.
    
    This wraps the NSUserDefaults class with a more friendly interface
    It is meant to be used like a dictionary"""
    
    def __init__(self, ud = None):
        if ud is None:
            from Foundation import NSUserDefaults
            self.ud = NSUserDefaults.standardUserDefaults()  
        else: self.ud = ud
            
    def __getitem__(self, key):
        return list(self.ud.arrayForKey_(key)) # could be a NSArray
        
    def __setitem__(self, key, value):
        self.ud.setValue_forKey_(value, key)
        self.ud.synchronize()
    
