__author__ = 'erik'

from PyQt4 import QtGui, QtCore

class WizardPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)
        self.setTitle('Upload to Bitbucket')

        grid = QtGui.QGridLayout()

        description = QtGui.QLabel('<qt><p>Enter your Bitbucket username and password below, '
                'as well as name for the repository and we\'ll upload it '
                'straight to Bitbucket!</p>\n'
                '<p>If you don\'t have a Bitbucket account yet, <a href="https://bitbucket.org/account/signup/">click here to '
                'sign up for free</a>.<p><qt>')
        description.setWordWrap(True)
        description.setOpenExternalLinks( True ) 
        grid.addWidget(description, 0, 0, 1, 3)

        username = QtGui.QLabel('Username or Email')
        grid.addWidget(username, 2, 0)
        usernameEdit = QtGui.QLineEdit()
        grid.addWidget(usernameEdit, 2, 1)

        password = QtGui.QLabel('Password')
        grid.addWidget(password, 3, 0)
        passwordEdit = QtGui.QLineEdit()
        passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        grid.addWidget(passwordEdit, 3, 1)

        repoName = QtGui.QLabel('Repository Name')
        grid.addWidget(repoName, 4, 0)
        repoName = QtGui.QLineEdit()
        grid.addWidget(repoName, 4, 1)

        self.setLayout(grid)
