__author__ = 'erik'

import sys
from PyQt4 import QtGui, QtCore

class SvnRepoPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)

        grid = QtGui.QGridLayout()

        description = QtGui.QLabel('Enter your Subversion repository location and credentials.')
        grid.addWidget(description, 0, 0, 1, 2)

        label = QtGui.QLabel('URL')
        grid.addWidget(label, 1, 0)
        urlEdit = QtGui.QLineEdit()
        grid.addWidget(urlEdit, 1, 1)
        QtGui.QWizardPage.registerField(self, 'url*', urlEdit)

        username = QtGui.QLabel('Username')
        grid.addWidget(username, 2, 0)
        usernameEdit = QtGui.QLineEdit()
        grid.addWidget(usernameEdit, 2, 1)
        QtGui.QWizardPage.registerField(self, 'username', usernameEdit)

        password = QtGui.QLabel('Password')
        grid.addWidget(password, 3, 0)
        passwordEdit = QtGui.QLineEdit()
        passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        grid.addWidget(passwordEdit, 3, 1)
        QtGui.QWizardPage.registerField(self, 'password', passwordEdit)

        self.setLayout(grid)


class UserMappingPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)

        grid = QtGui.QGridLayout()

        description = QtGui.QLabel('Specify username mappings below, or provide a mapping file.')
        grid.addWidget(description, 0, 0, 1, 2)

        self.setLayout(grid)


class OutputPage(QtGui.QWizardPage):

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


class ProgressPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)

        grid = QtGui.QGridLayout()

        description = QtGui.QLabel('Converting...')
        grid.addWidget(description, 0, 0, 1, 3)

        self.setLayout(grid)


app = QtGui.QApplication(sys.argv)

config = {}

wizard = QtGui.QWizard()
wizard.setWindowTitle('Subversion to Mercurial Converter')
wizard.addPage(SvnRepoPage())
wizard.addPage(UserMappingPage())
wizard.addPage(OutputPage())
wizard.show()

sys.exit(app.exec_())
