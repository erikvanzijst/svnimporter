#!/usr/bin/env python
#
# Copyright (C) 2007-9 Simon Edwards <simon@simonzone.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License or (at your option) version 2.1 or 
# version 3 or, at the discretion of KDE e.V. (which shall act as
# a proxy as in section 14 of the GPLv3), any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA  02110-1301 USA
#
import sys
import time
from PyQt4.uic.Compiler import indenter, compiler
from PyQt4.uic.Compiler import qtproxies
from PyQt4.uic.objcreator import MATCH,NO_MATCH

header = """#!/usr/bin/env python
# coding=UTF-8
#
# Generated by pykdeuic4 from %s on %s
#
# WARNING! All changes to this file will be lost.
from PyKDE4 import kdecore
from PyKDE4 import kdeui
"""
# Override how messages are translated.
original_i18n_string = qtproxies.i18n_string
class kde_i18n_string(qtproxies.i18n_string):
    def __init__(self,string):
        original_i18n_string.__init__(self,string)
    def __str__(self):
        return "kdecore.i18n(\"%s\")" % (qtproxies.escape(self.string),)
qtproxies.i18n_string = kde_i18n_string

def kdeFilter():
    import PyKDE4.kdeui
    import PyKDE4.kio

    # Load in the lists of KDE widgets.
    kde_widgets = {}
    for name,mod in [ ('PyKDE4.kdeui',PyKDE4.kdeui), ('PyKDE4.kio',PyKDE4.kio)]:
        for symbol in dir(mod):
            kde_widgets[symbol] = name

    def _kdefilter(widgetname, baseclassname, module):
        if widgetname in kde_widgets:
            return (MATCH, (widgetname, baseclassname, kde_widgets[widgetname]))
        else:
            return (NO_MATCH, None)
    return _kdefilter

def processUI(uifile, output_filename=None, exe=False, indent=4):
    
    if output_filename is not None:
        output = open(output_filename,'w')
    else:
        output = sys.stdout
    
    # Write out the header.
    output.write(header % (uifile,time.ctime()))
    indenter.indentwidth = indent
    comp = compiler.UICompiler()
    comp.factory._cwFilters.append(kdeFilter())
    winfo = comp.compileUi(uifile, output)

    if exe:
        output.write("""
if __name__ == '__main__':
    import sys
    global app
    class MainWin(kdeui.KMainWindow, """ + winfo['uiclass'] + """):
        def __init__ (self, *args):
            kdeui.KMainWindow.__init__ (self)
            rootWidget = QtGui.QWidget(self)
            self.setupUi(rootWidget)
            self.resize(640, 480)
            self.setCentralWidget(rootWidget)
    
    appName     = "default"
    catalog     = ""
    programName = kdecore.ki18n("default")
    version     = "1.0"
    description = kdecore.ki18n("Default Example")
    license     = kdecore.KAboutData.License_GPL
    copyright   = kdecore.ki18n("unknown")
    text        = kdecore.ki18n("none")
    homePage    = ""
    bugEmail    = "email"

    aboutData   = kdecore.KAboutData(appName, catalog, programName, version, description,
                              license, copyright, text, homePage, bugEmail)
    kdecore.KCmdLineArgs.init(sys.argv, aboutData)
    
    app = kdeui.KApplication()
    mainWindow = MainWin(None, "main window")
    mainWindow.show()
    app.connect (app, QtCore.SIGNAL ("lastWindowClosed ()"), app.quit)
    app.exec_ ()
""")

    if output_filename is not None:
        output.close()

def usage(rcode = 2):
    print("""Usage:
    pykdeuic4 [-h] [-e] [-o output_file] ui_file
Where:
    -h      Displays this message
    -e      Generate extra code to display the UI
    -o file Write the output to file instead of stdout
""")
    sys.exit(rcode)

def main():
    import getopt
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "o:eh")
    except getopt.GetoptError:
        usage()
        
    exe = False
    output_filename = None
    
    for opt, arg in optlist:
        if opt == "-h":
            usage(0)
        elif opt=="-e":
            exe = True
        elif opt=="-o":
            output_filename = arg
            
    if len(args)!=1:
        usage()

    processUI(args[0], output_filename, exe)
    
if __name__ == '__main__':
    main()
