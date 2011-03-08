import sys, util

__author__ = 'erik'

from PyQt4 import QtGui, QtCore
from restkit import request, BasicAuth
from restkit.forms import form_encode

class CREATE_RESULT:
    OK = 0
    UNAUTHORIZED = 1
    BAD_REQUEST = 2
    REMOTE_ERROR = 3
    UNKNOWN = 4
    desc = {
        OK: u'',
        UNAUTHORIZED: u'Username or password incorrect',
        BAD_REQUEST: u'Unable to create repository. Do you already have a '
                          'repository with this name?',
        REMOTE_ERROR: u'Unknown error while talking to Bitbucket',
        UNKNOWN: u'I have no idea what just went wrong..'
    }

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
        grid.addWidget(description, 0, 0, 1, 2)

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

        self.errorMessage = QtGui.QLabel()
        self.errorMessage.setWordWrap(True)
        grid.addWidget(self.errorMessage, 5, 1)

        self.setLayout(grid)

    def cleanupPage(self):
        self.errorMessage.clear()

    def validatePage(self):

        self.cleanupPage()

        # start the background job that logs us in
        self.job = WizardPage.CreateRepoTask(self)

        self.dialog = QtGui.QDialog(parent=self)
        self.dialog.setWindowTitle('Creating Bitbucket repository...')
        self.dialog.setWindowModality(QtCore.Qt.WindowModal)

        def reject():
            # user cannot press escape
            pass

        self.dialog.reject = reject

        spinner = QtGui.QLabel()
        movie = QtGui.QMovie('images/spinner-transparent.gif')
        spinner.setMovie(movie)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(QtGui.QLabel(u'Creating repository on Bitbucket'),
                         alignment=QtCore.Qt.AlignHCenter)
        layout.addWidget(spinner, alignment=QtCore.Qt.AlignHCenter)
        self.dialog.setLayout(layout)

        self.connect(self.job, QtCore.SIGNAL('done(int)'), self.dialog.done)

        movie.start()
        self.job.start()

        result = self.dialog.exec_()
        if result:
            self.errorMessage.setText(u'<p style="color: red;">%s</p>' % CREATE_RESULT.desc[result])
        return result == 0

    class CreateRepoTask(QtCore.QThread):

        def __init__(self, parent):
            QtCore.QThread.__init__(self)
            self.parent = parent

        def run(self):
            try:
                bb_username = str(QtGui.QWizardPage.field(self.parent, 'bb_username').toString())
                bb_password = str(QtGui.QWizardPage.field(self.parent, 'bb_password').toString())
                bb_reponame = str(QtGui.QWizardPage.field(self.parent, 'bb_reponame').toString())

                self.emit(QtCore.SIGNAL('done(int)'), self._create_repository(bb_username, bb_password, bb_reponame))

            except:
                type_, message, tb = sys.exc_info()
                print type_, message
                print util.traceback_to_str(tb)
                self.emit(QtCore.SIGNAL('done(int)'), CREATE_RESULT.UNKNOWN)

        def _create_repository(self, username, password, repo_name):
            '''Makes a REST call to Bitbucket to create the new remote repository
            before we can push.'''
            try:
                resp = request('https://api.bitbucket.org/1.0/repositories/',
                               method='POST',
                               body=form_encode({'name': repo_name}),
                               filters=[BasicAuth(username, password)],
                               headers={'Content-Type': 'application/x-www-form-urlencoded'},
                               follow_redirect=True)

                if resp.status_int == 401:
                    return CREATE_RESULT.UNAUTHORIZED
                elif resp.status_int == 400:
                    return CREATE_RESULT.BAD_REQUEST
                elif (resp.status_int // 100) != 2:
                    print 'Call failed:', resp.status_int, resp.body_string()
                    return CREATE_RESULT.REMOTE_ERROR
                else:
                    return CREATE_RESULT.OK
            except:
                type_, message, tb = sys.exc_info()
                print type_, message
                print util.traceback_to_str(tb)
                return CREATE_RESULT.UNKNOWN
