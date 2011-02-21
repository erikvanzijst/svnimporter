__author__ = 'erik'

from PyQt4 import QtGui

class WizardPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)

        grid = QtGui.QGridLayout()

        description = QtGui.QLabel('Converting...')
        grid.addWidget(description, 0, 0, 1, 3)

        self.setLayout(grid)
