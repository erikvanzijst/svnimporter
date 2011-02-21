__author__ = 'erik'

from PyQt4 import QtGui, QtCore

class WizardPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)

        grid = QtGui.QGridLayout()

        description = QtGui.QLabel('Specify a directory for the new Mercurial '
                'repository.\nMake sure you have enough space to hold the '
                'entire repository.')
        description.setWordWrap(True)
        grid.addWidget(description, 0, 0, 1, 3)

        dir = QtGui.QLabel('Save to')
        grid.addWidget(dir, 1, 0)
        self.dirEdit = QtGui.QLineEdit()
        grid.addWidget(self.dirEdit, 1, 1)
        QtGui.QWizardPage.registerField(self, 'output*', self.dirEdit)

        openFile = QtGui.QPushButton('Browse', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Select output directory')
        grid.addWidget(openFile, 1, 2)
        self.connect(openFile, QtCore.SIGNAL('clicked()'), self._showFileDialog)

        self.setLayout(grid)

    def _showFileDialog(self):
        self.dirEdit.setText(QtGui.QFileDialog.getExistingDirectory(self, 'Choose directory'))
