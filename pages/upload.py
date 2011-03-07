__author__ = 'erik'

from PyQt4 import QtGui, QtCore
from restkit import request, BasicAuth
from restkit.forms import form_encode

class RemoteException(Exception):
	'''Raised when a remote call failed.'''
	pass

class WizardPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)
        self.setTitle('Upload to Bitbucket')

        grid = QtGui.QGridLayout()

        description = QtGui.QLabel('<qt><p>Enter your Bitbucket username and password below, '
                'as well as a name for the new repository and we\'ll upload it '
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

	def _create_repository(self, username, password, repo_name):
		'''Makes a REST call to Bitbucket to create the new remote repository
		before we can push.'''
		resp = None
		try:
			resp = request('https://api.bitbucket.org/1.0/repositories/',
				method='POST',
				body=form_encode({'name': repo_name}),
				filters=[BasicAuth(username, password)],
				headers={'Content-Type': 'application/x-www-form-urlencoded'},
				follow_redirects=True)
		except:
			raise RemoteException()

		if (resp.status_int // 100) is not 2:
			raise RemoteException('Unexpected response: ' + resp.body_string)
