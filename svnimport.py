#!/usr/bin/env python

__author__ = 'erik'

import sys
from PyQt4 import QtGui
from pages import svnurl, mapping, output, importer, createrepo, upload

app = QtGui.QApplication(sys.argv)

wizard = QtGui.QWizard()
wizard.setWindowTitle('Subversion to Mercurial Converter')
wizard.addPage(svnurl.WizardPage())
wizard.addPage(mapping.WizardPage())
wizard.addPage(output.WizardPage())
wizard.addPage(importer.WizardPage())
wizard.addPage(createrepo.WizardPage())
wizard.addPage(upload.WizardPage())
wizard.show()

sys.exit(app.exec_())
