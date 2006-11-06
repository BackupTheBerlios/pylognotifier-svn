#
#  Notifier.py
#  LogNotifier
#
#  Created by Riko on 23/10/06.
#  Copyright (c) 2006 Enrico Franchi. All rights reserved.
#

import Growl
from Growl import GrowlNotifier, Image

logLabel   = 'logline'
errorLabel = 'error'
infoLabel  = 'info'

notifications = [logLabel, errorLabel, infoLabel]

def notifierFactory():
    '''Returns the configured notifier, according to environment.'''
    gn = GrowlNotifier(
        applicationName= 'LogNotifier', 
        notifications=   notifications, 
        applicationIcon= Image.imageWithIconForCurrentApplication()
    )
    gn.register()
    return gn
