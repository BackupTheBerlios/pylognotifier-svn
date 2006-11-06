#
#  Alarm.py
#  LogNotifier
#
#  Created by Riko on 23/10/06.
#  Copyright (c) 2006 Enrico Franchi. All rights reserved.
#

import time
import objc
from Foundation import NSTimer

def registerAlarm(subject, interval=0.5):
    '''Returns a correctly configured timer (already added to RunLoop, if Cocoa)'''
    return NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            interval, subject, 'alarm', objc.nil, objc.YES)

