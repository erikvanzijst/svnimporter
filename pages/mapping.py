__author__ = 'erik'

from PyQt4 import QtGui

class WizardPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)

        grid = QtGui.QGridLayout()

        description = QtGui.QLabel('Specify username mappings below, or provide a mapping file.')
        grid.addWidget(description, 0, 0, 1, 2)

        self.setLayout(grid)
