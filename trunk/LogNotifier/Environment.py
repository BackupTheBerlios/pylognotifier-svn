import os
import sys

#def _set_darwin():
#    pass
#
#def _log_factory(system):
#    try:
#        import Foundation
#        import AppKit
#        def Log(*args): 
#            from Foundation import NSLog
#            
#        
#    except ImportError:
#        
#        has_cocoa = False

class DarwinEnvironment(type):
    try:
        import Foundation
        import AppKit
        import objc
        has_cocoa = True
        def Log(cls, *args):
            from Foundation import NSLog
            NSLog(*args)
    except ImportError:
        has_cocoa = False
        def Log(*args): 
            print >> sys.stderr, args
    try:
        import Growl
        has_growl = True
    except ImportError:
        has_growl = False
    
        
    
class Environment(object):
    system = os.uname()
    __metaclass__ = eval('%sEnvironment' % system[0].capitalize())

              
            