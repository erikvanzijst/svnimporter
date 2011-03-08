__author__ = 'erik'

import time
from PyQt4 import QtGui, QtCore
from restkit import request, BasicAuth
from restkit.forms import form_encode

class UnauthorizedException(Exception):
    '''Raised from REST calls when a 401 is returned.'''
    pass

class RemoteException(Exception):
    '''Raised when a remote call failed.'''
    pass

class BadRequestException(Exception):
    pass

class WizardPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)
        self.setTitle('Upload to Bitbucket')

        grid = QtGui.QGridLayout()

        description = QtGui.QLabel('<qt><p>Enter your Bitbucket username and password below, '
                'as well as a name for the new repository and we\'ll upload it '
                'straight to Bitbucket!</p>\n'
                '<p>If you don\'t have a Bitbucket account yet, <a href="https://bitbucket.org/account/signup/">'
                'click here to sign up for free</a>.<p><qt>')
        description.setWordWrap(True)
        description.setOpenExternalLinks( True ) 
        grid.addWidget(description, 0, 0, 1, 3)

        username = QtGui.QLabel('Username or Email')
        grid.addWidget(username, 2, 0)
        usernameEdit = QtGui.QLineEdit()
        grid.addWidget(usernameEdit, 2, 1)
        QtGui.QWizardPage.registerField(self, 'bb_username*', usernameEdit)

        password = QtGui.QLabel('Password')
        grid.addWidget(password, 3, 0)
        passwordEdit = QtGui.QLineEdit()
        passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        grid.addWidget(passwordEdit, 3, 1)
        QtGui.QWizardPage.registerField(self, 'bb_password', passwordEdit)

        repoName = QtGui.QLabel('Repository Name')
        grid.addWidget(repoName, 4, 0)
        repoName = QtGui.QLineEdit()
        grid.addWidget(repoName, 4, 1)
        QtGui.QWizardPage.registerField(self, 'bb_reponame*', repoName)

        self.setLayout(grid)

    def validatePage(self):

        # start the background job that logs us in
        self.job = WizardPage.CreateRepoTask(self)
        self.connect(self.job, QtCore.SIGNAL('login_successful(PyQt_PyObject)'), self.login_successful)
        self.connect(self.job, QtCore.SIGNAL('login_failed(PyQt_PyObject)'), self.login_failed)
        self.job.start()
        return False

        print "validated!"

    def login_successful(self):
        '''Username and password worked, we created the new remote repo, so
        take us to the next screen and commence the push!'''

        print "Login successful."

    def login_failed(self, message):
        '''Print error message'''
        print 'Login failed: ' + message

    class CreateRepoTask(QtCore.QThread):

        # Signals:
        _progress = QtCore.pyqtSignal(int, name='progress')

        def __init__(self, parent):
            QtCore.QThread.__init__(self)

            self.parent = parent

            self.dialog = QtGui.QProgressDialog('Creating repository...', 'Cancel', 0, 2, parent=parent)
            self.dialog.setWindowModality(QtCore.Qt.WindowModal)
            self.dialog.setAutoClose(False)
            self.dialog.setAutoReset(False)

            self.connect(self, QtCore.SIGNAL('progress(int)'), self.dialog, QtCore.SLOT('setValue(int)'))
            self.connect(self, QtCore.SIGNAL('setLabel(const QString &)'), self.dialog, QtCore.SLOT('setLabelText(const QString &)'))
            self.dialog.show()

        def run(self):
            try:
                bb_username = str(QtGui.QWizardPage.field(self.parent, 'bb_username').toString())
                bb_password = str(QtGui.QWizardPage.field(self.parent, 'bb_password').toString())
                bb_reponame = str(QtGui.QWizardPage.field(self.parent, 'bb_reponame').toString())

                self._create_repository(bb_username, bb_password, bb_reponame)
                self.emit(QtCore.SIGNAL('login_successful(PyQt_PyObject)'), None)

            except UnauthorizedException:
                self.emit(QtCore.SIGNAL('login_failed(PyQt_PyObject)'),
                          u'Username or password incorrect.')
            except BadRequestException:
                self.emit(QtCore.SIGNAL('login_failed(PyQt_PyObject)'),
                          u'Unable to create repository. Do you already have a'
                          'repository named "%s"?' % bb_reponame)
            except:
                self.emit(QtCore.SIGNAL('login_failed(PyQt_PyObject)'),
                          u'Unknown error while talking to Bitbucket.')

        def _create_repository(self, username, password, repo_name):
            '''Makes a REST call to Bitbucket to create the new remote repository
            before we can push.'''
            try:
                resp = request('https://api.bitbucket.org/1.0/repositories/',
                               method='POST',
                               body=form_encode({'name': repo_name}),
                               filters=[BasicAuth(username, password)],
                               headers={'Content-Type': 'application/x-www-form-urlencoded'},
                               follow_redirects=True)

                if resp.status_int is 401:
                    raise UnauthorizedException()
                if resp.status.int is 400:
                    raise BadRequestException(resp.body_string)
                elif (resp.status_int // 100) is not 2:
                    raise RemoteException('Unexpected response: ' + resp.body_string)

            except (RemoteException, UnauthorizedException):
                raise
            except:
                raise RemoteException()

