#!/usr/bin/env python
#
# ------------------------------------------------
#
#   CHANGE ABOVE OR EDIT THE "Shell Script Files"
#   PHASE TO START THE THIS SCRIPT WITH ANOTHER
#   PYTHON INTERPRETER.
#
# ------------------------------------------------
# 

"""
Distutils script for building LogNotifier.

Development:
    xcodebuild -buildstyle Development

Deployment:
    xcodebuild -buildstyle Deployment

These will place the executable in
the "build" dir by default.

Alternatively, you can use py2app directly.
    
Development:
    python setup.py py2app --alias
    
Deployment:
    python setup.py py2app
    
These will place the executable in
the "dist" dir by default.

"""

from distutils.core import setup
import py2app
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from PyObjCTools import XcodeSupport

xcode = XcodeSupport.xcodeFromEnvironment(
    'LogNotifier.xcode',
    os.environ,
)

sys.argv = xcode.py2app_argv(sys.argv)
setup_options = xcode.py2app_setup_options('app')

infos = {
'author'           : 'Enrico Franchi',
'author_email'     : 'enrico.franchi@gmail.com' ,
'description'      : 'LogNotifier is a log presentation application that uses Growl.',
'keywords'         : 'logs, notifications, cocoa, growl',
'license'          : 'BSD license',
'name'             : 'LogNotifier',
'platforms'        : 'MacOS X',
'version'          : '0.3',
}

py2app_options = {
    'iconfile' : 'LogNotifier.icns',
    'plist'    : 'Info.plist'
}

setup_options.update(infos)
setup_options["options"]["py2app"].update(py2app_options)

setup(**setup_options)
