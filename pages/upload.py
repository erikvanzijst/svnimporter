from PyQt4 import QtGui, QtCore
from util import MercurialUI
from mercurial import hg, url as hg_url
import util
import sys

__author__ = 'erik'


class WizardPage(QtGui.QWizardPage):

    def __init__(self, *args, **kwargs):
        QtGui.QWizardPage.__init__(self, *args, **kwargs)


        self.setTitle('Pushing to Bitbucket')

        grid = QtGui.QGridLayout()

        self.description = QtGui.QLabel()
        self.description.setWordWrap(True)
        self.description.setOpenExternalLinks( True )
        grid.addWidget(self.description, 0, 0, 1, 2)

        self.logView = QtGui.QPlainTextEdit()
        self.logView.setReadOnly(True)
        grid.addWidget(self.logView, 1, 0)

        self.setLayout(grid)

    def initializePage(self):

        localDir = sys.argv[1]
        bb_username = 'evzijst'
        bb_password = 'pass'
        bb_reponame = sys.argv[2]
#        localDir = str(QtGui.QWizardPage.field(self.parent, 'localDir').toString())
#        bb_username = str(QtGui.QWizardPage.field(self.parent, 'bb_username').toString())
#        bb_password = str(QtGui.QWizardPage.field(self.parent, 'bb_password').toString())
#        bb_reponame = str(QtGui.QWizardPage.field(self.parent, 'bb_reponame').toString())
        url = u'https://bitbucket.org/%s/%s' % (bb_username, bb_reponame)

        self.description.setText('<qt><p>Pushing <b>%s</b> to <b>%s</b><p><qt>' % (localDir, bb_reponame))

        self.task = WizardPage.Task(self, **{
            'localDir': localDir,
            'bb_username': bb_username,
            'bb_password': bb_password,
            'bb_reponame': bb_reponame
            })
        self.connect(self, QtCore.SIGNAL('log(PyQt_PyObject)'), self.logView.appendHtml)
        self.task.start()

    def _info(self, msg):
        msg = str(msg)
        self.emit(QtCore.SIGNAL('log(PyQt_PyObject)'),
                  str('<div>%s</div>' % (msg[0:-1] if msg.endswith('\n') else msg)))

    def _error(self, msg):
        msg = str(msg)
        self.emit(QtCore.SIGNAL('log(PyQt_PyObject)'),
                  str(u'<div style="color: red">%s</div>' %
                      (msg[0:-1] if msg.endswith('\n') else msg)))

    def _job_finished(self):
        # TODO: disconnect signals
        pass

    class Task(QtCore.QThread):

        def __init__(self, widget, **opts):
            QtCore.QThread.__init__(self)
            self.widget = widget
            self.opts = opts

        def run(self):

            try:
                self.ui = MercurialUI()
                self.ui.logInfo = self.widget._info
                self.ui.logError = self.widget._error
                self.ui.setconfig('ui', 'interactive', 'off')
                self.ui.setconfig("ui", "formatted", None)
                self.ui.setconfig('ui', 'quiet', False)

                url = u'https://%s:%s@bitbucket.org/%s/%s' % (
                    self.opts['bb_username'],
                    self.opts['bb_password'],
                    self.opts['bb_username'],
                    self.opts['bb_reponame']
                )

                url = self.opts['bb_reponame']

                repo = hg.repository(self.ui, path=self.opts['localDir'], create=False)
                self.ui.write(u'Connecting to ' + hg_url.hidepassword(url))
                other = hg.repository(hg.remoteui(repo, {}), url)
                self.ui.write(u'pushing to %s\n' % hg_url.hidepassword(url))

                result = repo.push(other)
                print 'Push succeeded. Result code:', result

            except:
                type_, message, tb = sys.exc_info()
                print 'Push failed:', type_, message
                print util.traceback_to_str(tb)


