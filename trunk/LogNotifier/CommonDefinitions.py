try:
    import Foundation
    from Foundation import NSLog
    def Log(*args): NSLog(*args)
    
except ImportError:
    import sys
    def Log(*args): print >> sys.stderr, args
    