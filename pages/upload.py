__author__ = 'erik'

from PyQt4 import QtGui, QtCore

class WizardPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)
        self.setTitle('Pushing to Bitbucket')
