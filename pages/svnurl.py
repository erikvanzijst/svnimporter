__author__ = 'erik'

from PyQt4 import QtGui

class WizardPage(QtGui.QWizardPage):

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
