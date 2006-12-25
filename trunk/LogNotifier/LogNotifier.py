#
#  LogNotifier.py
#  LogNotifier
#

from PyObjCTools import NibClassBuilder, AppHelper
from Foundation import NSBundle, NSUserDefaults

info = NSBundle.mainBundle().infoDictionary()[u'PyObjCXcode']

for nibFile in info[u'NIBFiles']:
    NibClassBuilder.extractClasses(nibFile)

for pythonModule in info[u'Modules']:
    __import__(pythonModule)

if __name__ == '__main__':
    defaultValues = {
        u'MonitoredFiles':[
            { u'file'   : u'/var/log/system.log',
              u'sticky' : True}
        ]
    }
    NSUserDefaults.standardUserDefaults().registerDefaults_(defaultValues)
        
    AppHelper.runEventLoop()